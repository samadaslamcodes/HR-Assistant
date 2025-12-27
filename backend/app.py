from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from match import read_file, calculate_cv_jd_match
from document_validator import validate_cv, validate_jd

import json

# Adjust paths to point to frontend folder (sibling to backend)
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(base_dir, '..', 'frontend')
template_dir = os.path.abspath(os.path.join(frontend_dir, 'templates'))
static_dir = os.path.abspath(os.path.join(frontend_dir, 'static'))

# Global list to track candidates (in-memory for session)
# In production, this would be a database
processed_candidates = []

print(f"Template Dir: {template_dir}")
print(f"Static Dir: {static_dir}")

app = Flask(__name__, 
            template_folder=template_dir, 
            static_folder=static_dir)

app.secret_key = 'supersecretkey'  # Change this in production
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_match(cv_file, jd_text_input=None, jd_file=None, cv_filename_override=None):
    """Process a single CV against a JD (either text or file)."""
    cv_filename = cv_filename_override or secure_filename(cv_file.filename)
    cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
    cv_file.save(cv_path)
    
    jd_path = None
    try:
        # Read CV
        cv_text = read_file(cv_path)
        
        # Validate CV
        is_valid_cv, cv_conf, cv_reason = validate_cv(cv_text)
        if not is_valid_cv:
            return {"error": f"Invalid CV: {cv_reason}"}
        
        # Get JD text (either from text input or file)
        if jd_text_input:
            jd_text = jd_text_input
        elif jd_file:
            jd_filename = secure_filename(jd_file.filename)
            jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
            jd_file.save(jd_path)
            jd_text = read_file(jd_path)
        else:
            return {"error": "No job description provided"}
        
        # Validate JD
        is_valid_jd, jd_conf, jd_reason = validate_jd(jd_text)
        if not is_valid_jd:
            return {"error": f"Invalid Job Description: {jd_reason}"}
        
        # Calculate match
        results = calculate_cv_jd_match(cv_text, jd_text)
        results['cv_filename'] = cv_file.filename
        results['cv_internal_filename'] = cv_filename
        return results
        
    finally:
        # Clean up files
        try:
            # We keep the CV for downloading in the results page
            # if os.path.exists(cv_path): os.remove(cv_path) 
            if jd_path and os.path.exists(jd_path): os.remove(jd_path)
        except:
            pass

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("DEBUG: Upload request received")
        
        # Check if JD is provided as text or file
        jd_text_input = request.form.get('jd_text', '').strip()
        jd_file = request.files.get('jd')
        
        # Check if jd_file is actually empty (no file selected)
        jd_file_provided = jd_file and jd_file.filename != ''
        
        # Get CV files (can be multiple)
        cv_files = request.files.getlist('cv')
        
        print(f"DEBUG: JD text length: {len(jd_text_input)}, JD file provided: {jd_file_provided}")
        
        # Validation - either JD text or JD file must be provided
        if not cv_files or (not jd_text_input and not jd_file_provided):
            return render_template('upload.html', error='Please provide CV(s) and Job Description')
        
        # Filter out empty CV files
        cv_files = [f for f in cv_files if f.filename != '']
        if not cv_files:
            return render_template('upload.html', error='Please select at least one CV file')
        
        # JD text validation removed - allow any length
        
        # Validate file types
        for cv_file in cv_files:
            if not allowed_file(cv_file.filename):
                return render_template('upload.html', error=f'Invalid CV file type: {cv_file.filename}. Allowed: .txt, .pdf, .docx')
        
        if jd_file and jd_file.filename != '' and not allowed_file(jd_file.filename):
            return render_template('upload.html', error='Invalid JD file type. Allowed: .txt, .pdf, .docx')
        
        try:
            print(f"DEBUG: Processing {len(cv_files)} CV(s)...")
            
            # Process all CVs
            all_results = []
            for idx, cv_file in enumerate(cv_files):
                print(f"DEBUG: Processing CV {idx+1}/{len(cv_files)}: {cv_file.filename}")
                
                # Reset file pointers
                cv_file.seek(0)
                if jd_file_provided and not jd_text_input:
                    jd_file.seek(0)  # Reset JD file pointer for each CV
                
                # Process match
                result = process_match(
                    cv_file, 
                    jd_text_input=jd_text_input if jd_text_input else None,
                    jd_file=jd_file if jd_file_provided and not jd_text_input else None,
                    cv_filename_override=f"cv_{idx}_{secure_filename(cv_file.filename)}"
                )
                
                # Check for errors
                if isinstance(result, dict) and "error" in result:
                    return render_template('upload.html', error=result["error"])
                
                all_results.append(result)
            
            print(f"DEBUG: Processed {len(all_results)} CVs successfully")
            
            # Log to Admin Dashboard
            for res in all_results:
                cand_id = len(processed_candidates)
                processed_candidates.insert(0, {
                    "id": cand_id,
                    "name": res.get('candidate_name', 'Unknown'),
                    "filename": res.get('cv_filename', 'Unknown'),
                    "internal_filename": res.get('cv_internal_filename', 'Unknown'),
                    "score": res.get('match_percentage', 0),
                    "exp": res.get('experience_level', {}).get('cv', 'N/A'),
                    "full_results": res  # Store full results for the view details button
                })
            
            # Sort by match percentage (highest first)
            all_results.sort(key=lambda x: x.get('match_percentage', 0), reverse=True)
            
            # If single CV, show single result page
            if len(all_results) == 1:
                return render_template('results.html', results=all_results[0])
            
            # If multiple CVs, show batch results
            return render_template('batch_results.html', results=all_results, total_cvs=len(all_results))
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"ERROR: {e}")
            return render_template('upload.html', error=f'Processing failed: {str(e)}')
            
    return render_template('upload.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', candidates=processed_candidates)

@app.route('/admin/analysis/<int:cand_id>')
def view_analysis(cand_id):
    # Find candidate by ID
    candidate = next((c for c in processed_candidates if c['id'] == cand_id), None)
    if not candidate:
        return "Candidate not found", 404
    return render_template('results.html', results=candidate['full_results'])

@app.route('/admin/delete/<int:cand_id>', methods=['POST'])
def delete_candidate(cand_id):
    global processed_candidates
    processed_candidates = [c for c in processed_candidates if c['id'] != cand_id]
    return redirect(url_for('admin'))

@app.route('/download/<path:filename>')
def download_cv_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/api/match', methods=['POST'])
def api_match():
    if 'cv' not in request.files or 'jd' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    cv = request.files['cv']
    jd = request.files['jd']
    
    if cv.filename == '' or jd.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if cv and allowed_file(cv.filename) and jd and allowed_file(jd.filename):
        try:
            results = process_match(cv, jd)
            if "error" in results:
                return jsonify(results), 400
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
