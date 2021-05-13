from flask import render_template, request, redirect, url_for
from flask_app import app
import re
import os
from werkzeug.utils import secure_filename

file_path_file = open('flask_app/file_path.txt', 'r')
paths = file_path_file.readlines()
image_path = ""
for path in paths:
    path = re.search("((?<=IMAGE_UPLOADS>).+)", path)
    if path:
        image_path = path[0]
        break
print("image path is " + image_path)
app.config["IMAGE_UPLOADS"] = image_path
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG"]
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


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
    print(f'success! {filename}')
    return render_template('success.html', filename=filename)


# @app.route('/display/<filename>')
def display_image(filename):
    print(filename)
    return redirect(url_for('static', filename='uploaded_images/' + filename), code=301)


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    attr = "IMAGE_UPLOADS"
                    image.save(os.path.join(app.config[attr], filename))
                    print("Image saved")
                    print(f"upload_image: {filename}")
                    # return redirect(request.url)
                    return render_template('success.html', filename=filename)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)
    return render_template("upload_image.html")
