#!flask/bin/python
from flask import Flask
from flask import jsonify, request
from flask import abort, make_response
from shamir_shares import *
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/generate_mnemonics', methods=['POST'])
def generate_mnemonics():
    if not request.json:
        abort(400)
    return request.json

@app.route('/generate_shares', methods=['POST'])
def generate_shares():
    """
    Generate Shamir 39 shares from the given mnemonic
    """
    if not request.json:
        abort(400)

    mnemonics = request.json["mnemonics"]
    m = request.json["m"]
    n = request.json["n"]
    shamir_shares = split_shares(mnemonics, m, n)

    print(mnemonics, m, n)
    return jsonify(shares=shamir_shares)

@app.route('/')
def index():
    return "Welcome to Shamir Secret Sharing App"


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

if __name__ == '__main__':
    app.run(debug=True)