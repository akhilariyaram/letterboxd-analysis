import os
import shutil
import zipfile
from flask import Flask, request, redirect, url_for, render_template, jsonify
from utils.parser import load_and_merge_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_zip():
    zip_file = request.files['zipfile']

    if zip_file.filename.endswith('.zip'):
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], 'letterboxd.zip')

        # 🔥 Clear old files safely
        for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"❌ Could not delete {file}: {e}")

        # Save zip file
        zip_file.save(zip_path)

        # Extract contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(app.config['UPLOAD_FOLDER'])

        return redirect(url_for('dashboard'))

    return 'Invalid file format. Please upload a ZIP file.'

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    data = load_and_merge_data(app.config['UPLOAD_FOLDER'])
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
