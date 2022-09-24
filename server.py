from flask import Flask, request
import urllib.request
from config import models_dir, server_port
from lib.file_service import list_dir, File

app = Flask(__name__)

file = File

@app.route('/', methods=['GET'])
def index():
    return list_dir(models_dir)
 
@app.route('/<path:path>', methods=['GET'])
def serve(path):
  return file.getFile(path)

@app.route('/file-upload', methods=['POST'])
def upload_file():
  return file.upload_file(request.files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=server_port)