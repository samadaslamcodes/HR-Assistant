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
    
    cv_text = read_file(cv_path)
    jd_text = read_file(jd_path)
    
    results = calculate_cv_jd_match(cv_text, jd_text)
    
    # Clean up files
    try:
        os.remove(cv_path)
        os.remove(jd_path)
    except:
        pass
        
    return results

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'cv' not in request.files or 'jd' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        cv = request.files['cv']
        jd = request.files['jd']
        
        if cv.filename == '' or jd.filename == '':
            flash('No selected file')
            return redirect(request.url)
            
        if cv and allowed_file(cv.filename) and jd and allowed_file(jd.filename):
            results = process_match(cv, jd)
            return render_template('results.html', results=results)
        else:
            flash('Allowed file types are .txt, .pdf, .docx')
            return redirect(request.url)
            
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
