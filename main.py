import os

from flask import Flask, request
from werkzeug.utils import secure_filename

from utilities.file import check_create_dir
from utilities.runner import Runner

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'input')
OUTPUT_DIR_PATH = os.path.join(os.getcwd(), 'output')
runner = Runner()


check_create_dir(UPLOAD_FOLDER)
check_create_dir(OUTPUT_DIR_PATH)

import io
from base64 import encodebytes
from PIL import Image
from flask import jsonify
import os, shutil

def clean_input():
  for filename in os.listdir(UPLOAD_FOLDER):
      file_path = os.path.join(UPLOAD_FOLDER, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))

def get_response_image(image_path: str):
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


@app.route('/predict', methods=['POST'])
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
    
    runner.run_model(UPLOAD_FOLDER, OUTPUT_DIR_PATH)
    
    encoded_imges = []
    added_prediction_path = os.path.join(OUTPUT_DIR_PATH, 'added_prediction')
    
    for image_path in os.listdir(added_prediction_path):      
      encoded_imges.append(get_response_image(os.path.join(added_prediction_path, image_path)))
    clean_input()
    return jsonify({'result': encoded_imges})

def create_app():
   return app

if __name__ == '__main__':
    app.run(debug=True)
