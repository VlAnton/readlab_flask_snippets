from flask import Flask

from app import app as snippets_app

import logging


app = Flask(__name__)
app.register_blueprint(snippets_app)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    app.run(host='0.0.0.0', debug=True)