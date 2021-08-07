import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory

from werkzeug.utils import secure_filename

from scan import decode_barcode
UPLOAD_FOLDER = './images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html', text="Hello, world")

@app.route("/can")
def can():
    return render_template('can.html')

@app.route("/cannot")
def cannot():
    return render_template('cannot.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(decode_barcode(os.path.join(".",app.config['UPLOAD_FOLDER'],
                               filename)))

            return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)