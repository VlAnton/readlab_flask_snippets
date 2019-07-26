from flask import Blueprint, jsonify, request, redirect, url_for
from psycopg2 import InternalError, ProgrammingError

import logging

from storage.postgres import postgres


app = Blueprint('snippets-api', __name__)


@app.after_request
def cors(res):
    headers = res.headers
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Methods'] = 'GET, POST'
    headers['Access-Control-Allow-Headers'] = '*'

    return res

@app.route('/api/')
@app.route('/api')
def index():
    return redirect(url_for('snippets-api.get_post_snippets'))


@app.route('/api/snippets/', methods=['GET', 'POST'])
@app.route('/api/snippets', methods=['GET', 'POST'])
def get_post_snippets():
    if request.method == 'GET':
        snippets: list = postgres.get_snippets()

        return jsonify(snippets)

    dict_args = dict()

    for field, value in request.form.items():
        dict_args[field] = value

    postgres.create_snippet(request, **dict_args)

    return jsonify('Snippet is successfully created')


@app.route('/api/snippets/<uid>/')
@app.route('/api/snippets/<uid>')
def retrieve_snippet(uid: str):
    snippet: dict = postgres.retrieve_snippet(uid)
    print(snippet)

    return jsonify(snippet)