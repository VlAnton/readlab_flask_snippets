from flask import Blueprint, jsonify, request, Request

from psycopg2 import InternalError, ProgrammingError

import logging

from storage.postgres import postgres


app = Blueprint('snippets', __name__)


@app.route('/snippets')
def get_snippets():
    snippets: list = postgres.get_snippets()

    return jsonify(snippets)

@app.route('/snippets', methods=['POST'])
def create_snippet():
    dict_args = dict()
    # print(request.form)

    for field, value in request.form.items():
        dict_args[field] = value

    postgres.create_snippet(request, **dict_args)

    return jsonify('Snippet is successfully created')

@app.route('/snippets/<uid>')
def retrieve_snippet(uid: str):
    snippet: dict = postgres.retrieve_snippet(uid)
    print(snippet)

    return jsonify(snippet)