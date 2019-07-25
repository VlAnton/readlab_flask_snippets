from flask import Flask, render_template

from api import app as snippets_api

import logging
import os


app = Flask(__name__)
app.register_blueprint(snippets_api)


# @app.route('/<name>', methods=['GET'])
# def snippets_list(name: str):        
#     return render_template('snippets.html', name=name)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    app.run(host='0.0.0.0', debug=True)