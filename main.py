import os
import traceback

from flask import Flask, send_file, request, jsonify
from werkzeug.utils import secure_filename, send_from_directory
from pdf2docx import Converter

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return send_file('templates/index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if filename.endswith('.pdf'):
                docx_filename = filename.replace('.pdf', '.docx')
                docx_filepath = filepath.replace('.pdf', '.docx')

                cv = Converter(filepath)
                cv.convert(docx_filepath, start=0, end=None)
                cv.close()

                return send_file(docx_filepath, as_attachment=True)
            elif filename.endswith('.docx'):
                return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        print(f"Error during conversion: {e}")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during file conversion', 'details': str(e)}), 500

def run_app():
    app.run(debug=True, port=int(os.environ.get('PORT', 80)))

if __name__ == '__main__':
    run_app()

# Dependencies are installed and can be removed
