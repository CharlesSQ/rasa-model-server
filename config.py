from os import environ
from flask import Flask

models_dir = environ.get('MODELS_DIR', 'models')
server_port = environ.get('PORT', 5001)


UPLOAD_FOLDER = 'models/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024