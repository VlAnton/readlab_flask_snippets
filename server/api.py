from flask import Blueprint, jsonify, request, redirect, url_for, Request
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

@app.route('/api/snippets/', methods=['GET', 'POST'])
@app.route('/api/snippets', methods=['GET', 'POST'])
def get_post_snippets():
    if request.method == 'GET':
        snippets = postgres.get_snippets()
        return jsonify(snippets)
    try:
        postgres.create_snippet(request, **request.form)
        return jsonify('Snippet is successfully created')
    except Exception as err:
        return jsonify(str(err))


@app.route('/api/snippets/<uid>/')
@app.route('/api/snippets/<uid>')
def retrieve_snippet(uid: str):
    snippet: dict = postgres.retrieve_snippet(uid)
    return jsonify(snippet)
