import binascii
import math
import struct

from flask import abort

from wordlist.wordlist_english import ENGLISH_WORDLIST
# from secretsharing import SecretSharer
from secretsharing import PlaintextToHexSecretSharer

def split_shares(mnemonics, m, n):
    """
    Split BIP39 mnemonics into Shamir Shares

    @param mnemonic_words - BIP39 Mnemonic words
    @param m - must require number of shares
    @param n - number of shares to be created

    """
    if m < 2 :
        abort(400, {'message': "Must require at least 2 shares"})
    if n < 2 :
        abort(400, {'message': "Must split to at least 2 shares"})
    if m > 4095 :
        abort(400, {'message': "Must require at most 4095 shares"})
    if n > 4095 :
        abort(400, {'message': "Must split to at most 4095 shares"})

    if len(mnemonics.split(" ")) == 0 :
        abort(400, {'message': "BIP39 Mnemonic words not provided!"})

    mnemonics = mnemonics.encode("ascii")
    
    shamir_shares = PlaintextToHexSecretSharer.split_secret(mnemonics, m, n)
    return shamir_shares


