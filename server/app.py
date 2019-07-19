from flask import Blueprint, jsonify, request

from psycopg2 import InternalError, ProgrammingError

import logging

# from storage import postgres
from storage.postgres import postgres


app = Blueprint('snippets', __name__)


@app.route('/snippets')
def get_snippets():
    snippets = postgres.get_snippets()

    return jsonify(snippets)

@app.route('/snippets', methods=['POST'])
def create_snippet():
    request_json = request.args
    # print(['code'])

    description = request_json['description']
    code = request_json['code']
    url = request_json['url']

    postgres.create_snippet(code, description, url)

    return jsonify('Snippet is successfully created')