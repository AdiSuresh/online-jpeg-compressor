from flask import render_template, request, redirect
from flask_app import app
import re
import os


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


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print("Image saved")
            print(image)
            return redirect(request.url)
    return render_template("upload_image.html")
