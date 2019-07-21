from flask import Blueprint, jsonify, request, Request

from psycopg2 import InternalError, ProgrammingError

import logging

from storage.postgres import postgres


app = Blueprint('snippets', __name__)


@app.route('/snippets')
def get_snippets():
    snippets = postgres.get_snippets()

    return jsonify(snippets)

@app.route('/snippets', methods=['POST'])
def create_snippet():
    dict_args = dict()

    for field, value in request.form.items():
        dict_args[field] = value

    postgres.create_snippet(request, **dict_args)

    return jsonify('Snippet is successfully created')