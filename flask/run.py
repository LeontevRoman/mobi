from flask import Flask, render_template
from settings import Config

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/upload')
def upload():
    return render_template('upload.html', fastapi_url=Config.FASTAPI_URL)


@flask_app.route('/show')
def show():
    return render_template('list_images.html', fastapi_url=Config.FASTAPI_URL)


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8000, debug=False)
