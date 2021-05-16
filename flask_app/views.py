from flask import render_template, request, redirect, url_for, send_file
from flask_app import app
import re
import os
from werkzeug.utils import secure_filename
import numpy as np
import cv2 as cv
from flask_mail import Message, Mail

file_path_file = open('flask_app/file_path.txt', 'r')
vars = file_path_file.readlines()


def get_req_var(var):
    result = 0
    for s in vars:
        s = re.search("((?<=" + var + ">).+)", s)
        if s:
            result = s[0]
            break
    return result


image_path = get_req_var("IMAGE_UPLOADS")
app.config["IMAGE_UPLOADS"] = image_path
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["MAX_IMAGE_FILESIZE"] = 50 * 1024 * 1024

# for mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = get_req_var("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = get_req_var("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# for mail


@app.route('/')
def home():
    return render_template('index.html')


def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


def allowed_image(filename):
    # We only want files with a . in the filename
    if "." not in filename:
        return False
    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]
    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/success')
def success(filename):
    return render_template('success.html', filename=filename)


@app.route('/display/<filename>')
def display_image(filename):
    filename = 'uploaded_images/' + filename
    return redirect(url_for('static', filename=filename), code=301)


@app.route("/download/<filename>")
def download_image(filename):
    filename = 'static/uploaded_images/' + filename
    return send_file(filename, as_attachment=True)


@app.route("/send-mail/<filename>")
def send_mail(filename):
    filename = 'static/uploaded_images/' + filename
    mail = Mail(app)
    mail.init_app(app)
    msg = Message(
        "Sent from flask_app",
        sender=app.config["MAIL_USERNAME"],
        recipients=["adithyasuresh201@gmail.com",
                    "adithyansraj20@gmail.com", app.config["MAIL_USERNAME"]],
    )
    with app.open_resource(filename) as fp:
        msg.attach("image.jpg", "image/jpg", fp.read())
    mail.send(msg)
    return render_template("mail_sent.html")


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    # cwd = os.path.join(os.getcwd(), image_path)
    # print(cwd)
    for f in os.listdir(image_path):
        os.remove(os.path.join(image_path, f))
        print(f"file {f}")
        print(image_path)
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    img = np.fromfile(image, np.uint8)
                    img = cv.imdecode(img, cv.IMREAD_COLOR)
                    quality = 80
                    quality_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
                    img_path = app.config["IMAGE_UPLOADS"] + "/" + filename
                    cv.imwrite(img_path, img, quality_param)
                    return render_template('success.html', filename=filename)

                else:
                    return redirect(request.url)
    return render_template("upload_image.html")
