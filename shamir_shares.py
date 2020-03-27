import binascii
import math
import struct

from flask import abort

from wordlist.wordlist_english import ENGLISH_WORDLIST


def split_shares(mnemonic_words, m, n):
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

    if len(mnemonic_words) == 0 :
        abort(400, {'message': "BIP39 Mnemonic words not provided!"})

    bin_str = ""

    for word in mnemonic_words:
        word_index = ENGLISH_WORDLIST.index(word)
        if word_index < 0 :
            abort(400, {'message': 'Invalid word found in the list: '+ word})
        
        index_bits = struct.pack("i", word_index)
        index_bits_padded = index_bits.ljust(11, "0")
        bin_str += index_bits_padded
    
    hex_str = binascii.hexlify(bin_str)
    print(hex_str)