from flask import render_template, send_from_directory
import os
from os import sep
from os.path import isdir, dirname, basename, relpath, join, exists
from config import models_dir, app
from lib.file_system import Scaner
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['tar', 'gz'])

class File:
  def get_file(self, path):
    fetch_latest = '@latest' in path
    real_path = join(models_dir, path.replace('@latest', ''))
    
    if not exists(real_path):
        return 'Not Found', 404

    if isdir(real_path):
        if fetch_latest:
            latest_entry = Scaner(real_path).latest_entry
            if not latest_entry:
                return 'No Models Found', 404
            return download_file(latest_entry.path)
        else:
            return list_dir(real_path)
    else:
      
        return download_file(real_path)
  
  def upload_file(self, files):
    # check if the post request has the file part
    if 'file' not in files:
      return 'No file part in the request', 400
    file = files['file']
    if file.filename == '':
      return 'No file selected for uploading', 400
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return 'File successfully uploaded', 201
    else:
      return 'Allowed file type is tar.gz', 400

def list_dir(path):
    rel_path = relpath(path, models_dir)
    parent_path = dirname(rel_path)
    return render_template('index.html', sep=sep, parent_path=parent_path, path=rel_path, entries=Scaner(path).entries)

def download_file(path):
    print(dirname(path))
    print(basename(path))
    return send_from_directory(dirname(path), basename(path), as_attachment=True)

def allowed_file(filename):
    filename_components = filename.rsplit('.')
    print(filename_components)
    return '.' in filename and filename_components[1].lower() in ALLOWED_EXTENSIONS \
      and filename_components[2].lower() in ALLOWED_EXTENSIONS
