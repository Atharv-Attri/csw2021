import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory

from werkzeug.utils import secure_filename

from scan import decode_barcode
import converter
UPLOAD_FOLDER = 'static/image'
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

@app.route("/compost")
def compost():
    return render_template('compost.html')

@app.route("/nah")
def nah():
    return render_template('nah.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/404")
def four_oh_four():
    return render_template('404.html')

@app.route("/notindata")
def notindata():
    return render_template('notindata.html')


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
            barcode = decode_barcode(os.path.join(".",app.config['UPLOAD_FOLDER'],
                               filename))
            if barcode == "0":
                    return render_template('404.html', image=url_for('static', filename='image/'+filename))


            title = converter.get_title(barcode)
            title_type = converter.get_type(title)
            if title_type == "ewaste":
                return render_template('ewaste.html', title=title, image=url_for('static', filename='image/'+filename))
            elif title_type == "recycle":
                return render_template('can.html', title=title, image=url_for('static', filename='image/'+filename))
            elif title_type == "compostable":
                return render_template('compost.html', title=title, image=url_for('static', filename='image/'+filename))
            elif title_type == "trash":
                return render_template('cannot.html', title=title, image=url_for('static', filename='image/'+filename))
            if title_type == "not in our database":
                return render_template('notindata.html', title=title, image=url_for('static', filename='image/'+filename))
            else:
                return render_template('nah.html', title=title, image=url_for('static', filename='image/'+filename))
            
            