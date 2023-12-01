import io
import os
import zipfile

from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = './input'
PROCESSED_FOLDER = './output'


@app.route('/get_processed_images', methods=['GET'])
def get_processed_images():
    # Create a zip file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for filename in os.listdir(PROCESSED_FOLDER):
            zf.write(os.path.join(PROCESSED_FOLDER, filename), filename)

    memory_file.seek(0)

    return send_file(memory_file, attachment_filename='processed_images.zip', as_attachment=True)


@app.route('/upload', methods=['POST'])
def predict():
    if 'files[]' not in request.files:
        return "No file part in the request", 400

    files = request.files.getlist('files[]')

    for file in files:
        if file.filename == '':
            return "No selected file", 400

        if file:  # If the file is valid
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

    return "Files Uploaded Successfully", 200


@app.route('/')
def index():
    return "Welcome to the Image Processing Server!"


if __name__ == '__main__':
    app.run(debug=True)
