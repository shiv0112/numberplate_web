from flask import Flask, render_template, request
import requests
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import prediction

app = Flask(__name__, template_folder='.')
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'static')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

BASE_DIR = os.getcwd()
dir = os.path.join(BASE_DIR, "uploads")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def homepage():
  return render_template('templates/index.html')

@app.route('/uploaded', methods = ['GET','POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(UPLOAD_FOLDER+'\\'+"new.mp4")
      return render_template('templates/upload.html')
   else:
      return 'File not uploaded'

@app.route('/model_predict', methods = ['GET','POST'])
def predict():
  return render_template('templates/model.html')

@app.route('/detect')
def detect():
  return(prediction.final())

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)