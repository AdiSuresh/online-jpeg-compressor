from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    return render_template('upload_image.html')


if __name__ == '__main__':
    app.run(debug=True)
