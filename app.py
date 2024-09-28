from flask import Flask, request, jsonify, render_template
from detector import detect_code_smells
from duplicates import detect_duplicates

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.py'):
        source_code = file.read().decode('utf-8')  # Decode the file contents to a string
        smells = detect_code_smells(source_code, file.filename)  # Pass source code and filename
        duplicates = detect_duplicates(source_code, file.filename)
        
        return jsonify(smells, duplicates), 200
    
    return jsonify({'error': 'Invalid file format. Only .py files are allowed.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
