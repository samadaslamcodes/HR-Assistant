import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from match import read_file, calculate_cv_jd_match

# Adjust paths to point to frontend folder (sibling to backend)
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(base_dir, '..', 'frontend')
template_dir = os.path.abspath(os.path.join(frontend_dir, 'templates'))
static_dir = os.path.abspath(os.path.join(frontend_dir, 'static'))

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

def process_match(cv_file, jd_file):
    cv_filename = secure_filename(cv_file.filename)
    jd_filename = secure_filename(jd_file.filename)
    
    cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)
    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
    
    cv_file.save(cv_path)
    jd_file.save(jd_path)
    
    try:
        cv_text = read_file(cv_path)
        jd_text = read_file(jd_path)
        
        results = calculate_cv_jd_match(cv_text, jd_text)
        return results
        
    finally:
        # Clean up files regardless of success/fail
        try:
            if os.path.exists(cv_path): os.remove(cv_path)
            if os.path.exists(jd_path): os.remove(jd_path)
        except:
            pass

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("DEBUG: Upload request received")
        if 'cv' not in request.files or 'jd' not in request.files:
            return render_template('upload.html', error='Missing file parts')
        
        cv = request.files['cv']
        jd = request.files['jd']
        
        print(f"DEBUG: CV={cv.filename}, JD={jd.filename}")

        if cv.filename == '' or jd.filename == '':
            return render_template('upload.html', error='Please select both files')
            
        if cv and allowed_file(cv.filename) and jd and allowed_file(jd.filename):
            try:
                print("DEBUG: Processing match...")
                results = process_match(cv, jd)
                print("DEBUG: Match processed successfully")
                
                # Check for explicit errors returned by process_match
                if isinstance(results, dict) and "error" in results:
                     return render_template('upload.html', error=results["error"])

                return render_template('results.html', results=results)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"ERROR: {e}")
                return render_template('upload.html', error=f"An error occurred during analysis: {str(e)}")
        else:
            return render_template('upload.html', error='Invalid file type. Allowed: .txt, .pdf, .docx')
            
    return render_template('upload.html')

@app.route('/about')
def about():
    return render_template('about.html')

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
