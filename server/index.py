from flask import Flask

from app import app as snippets_app

import logging
import os


MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOAD_FOLDER = os.path.join(__file__) + 'uploads'

app = Flask(__name__)
app.register_blueprint(snippets_app)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    app.run(host='0.0.0.0', debug=True)