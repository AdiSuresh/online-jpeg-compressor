from flask import render_template
from flask_app import app


@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    return render_template('upload_image.html')


if __name__ == '__main__':
    app.run(debug=True)
