#!flask/bin/python
from flask import Flask
from flask import jsonify, request
from flask import abort, make_response
from shamir39.shamir_shares import split_shares, combine_shares, generate
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


@app.route('/generate_mnemonics', methods=['POST'])
def generate_mnemonics():
    """
    Generate a new set of BIP 39 mnemonics
    """
    if not request.json:
        number_of_words = 12
    
    number_of_words = request.json["number_of_words"]
  
    new_mnemonic = generate(number_of_words)
    return jsonify(mnemonic=new_mnemonic)


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


@app.route('/recover_secret', methods=['POST'])
def recover_secret():
    """
    Recover the secret key from the provided shares
    """
    if not request.json:
        abort(400)
    
    shamir_shares = request.json["shares"]

    recovered_key = combine_shares(shamir_shares)
    return jsonify(recovered_key=recovered_key)


@app.route('/')
def index():
    return "Welcome to Shamir Secret Sharing App"


@app.errorhandler(Exception)
def handle_error(e):
    """
    Error handling function that sends the error back as an HTTP response
    """
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


if __name__ == '__main__':
    app.run(debug=True)