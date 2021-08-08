import glob
import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import converter
from scan import decode_barcode

# Set Flask settings
UPLOAD_FOLDER = "static/image"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# get data
with open("alter.json", "r") as f:
    alter = json.loads(f.read())

# Set list of allowed files to keep the app secure
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# route to the homepage
@app.route("/")
def index():
    return render_template("index.html", text="Hello, world")


#! THE FOLLOWING ROUTES ARE NOT MEANT TO BE ACCESSED BY THE USER!!
#! THEY ARE LEFT OPEN FOR YOU TO JUDGE!!

# routes to the can be recycled page
@app.route("/can")
def can():
    return render_template("can.html")

# routes to the can't be recycled page
@app.route("/cannot")
def cannot():
    return render_template("cannot_plain.html")

# routes to the can be composted page
@app.route("/compost")
def compost():
    return render_template("compost.html")

# routes to the we aren't sure if it can be recycled page
@app.route("/nah")
def nah():
    return render_template("nah.html")

# routes to the about us page
@app.route("/about")
def about():
    return render_template("about.html")

# routes to the we could not find it in our data page
@app.route("/404")
def four_oh_four():
    return render_template("404.html")

# Route to the error page that the info is not in the database
@app.route("/notindata")
def notindata():
    return render_template("notindata.html")

# Deals with our database not having organic products
@app.route("/compost-static")
def compost_static():
    return render_template("compost-static.html"

#Route for ewaste
@app.route("/ewaste")
def ewaste():
    return render_template("ewaste.html")


# Deals with uploading the images
# and then redirecting the user to the correct page
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    files = glob.glob("static/image/*") #deletion of all files in the folder, keeps it clean
    for f in files:
        os.remove(f)
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also must
        # submit a empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            barcode = decode_barcode(
                os.path.join(".", app.config["UPLOAD_FOLDER"], filename)
            )
            if barcode == "0":
                return render_template(
                    "404.html", image=url_for("static", filename="image/" + filename)
                )

            title = converter.get_title(barcode)
            title_type = converter.get_type(title)
            if title_type[0] == "ewaste":
                return render_template(
                    "ewaste.html",
                    title=title,
                    image=url_for("static", filename="image/" + filename),
                )

            elif title_type[0] == "compostable":
                return render_template(
                    "compost.html",
                    title=title,
                    image=url_for("static", filename="image/" + filename),
                )
            elif title_type[0] == "trash":
                global alter
                try:
                    return render_template(
                        "cannot.html",
                        title=title,
                        image=url_for("static", filename="image/" + filename),
                        data=alter[title_type[1]],
                    )
                except KeyError:
                    return render_template(
                        "cannot_plain.html",
                        title=title,
                        image=url_for("static", filename="image/" + filename),
                    )
            elif title_type[0] == "recycle":
                return render_template(
                    "can.html",
                    title=title,
                    image=url_for("static", filename="image/" + filename),
                )
            else:
                return render_template(
                    "nah.html",
                    title=title,
                    image=url_for("static", filename="image/" + filename),
                )
