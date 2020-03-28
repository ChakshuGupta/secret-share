import binascii
import math
import struct

from flask import abort

from wordlist.wordlist_english import ENGLISH_WORDLIST
from pyseltongue import SecretSharer


def split_shares(mnemonics, m, n):
    """
    Split BIP39 mnemonics into Shamir Shares

    @param mnemonic_words - BIP39 Mnemonic words
    @param m - must require number of shares
    @param n - number of shares to be created

    """
    mnemonic_words = mnemonics.split(" ")

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
        if word_index < 0:
            error_message = "Invalid word found in the mnemonics: " + word
            abort(400, {'message': error_message})
        index_bits =  "{0:b}".format(word_index)
        index_bits = index_bits.rjust(11, '0')
        print(index_bits, len(index_bits))
        bin_str += index_bits
    
    hex_str = hex(int(bin_str, 2))
    hex_str = hex_str.split("x")[1]
    print(hex_str, len(hex_str))

    shamir_shares = SecretSharer.split_secret(hex_str, m, n)
    print(shamir_shares)
    shamir39_mnemonics  = list()
    for share in shamir_shares:
        shamir39_mnemonics.append(shares_to_shamir39_mnemonics(share))

    return shamir39_mnemonics


def shares_to_shamir39_mnemonics(shamir_share):
    """
    Convert the shamir share to shamir39 mnemonic words

    @param shamir_share
    """
    share_number, share = shamir_share.split("-")
    print(share_number)
    share_binary = bin(int(share, 16))
    share_binary = share_binary.split("b")[1]
    new_mnemonic = bin_to_mnemonics(share_binary)
    print(new_mnemonic)
    return new_mnemonic


def bin_to_mnemonics(bin_str):
    """
    Convert binary string to mnemonics
    
    @param bin_str: Binary string
    """
    mnemonic = list()

    total_words = int(math.ceil(len(bin_str)/11))
    total_bits = total_words * 11
    print(total_words, total_bits)
    bin_str = bin_str.rjust(total_bits, '0')
    for i in range(0, total_words):
        sub_bin_str = bin_str[i*11 : (i+1)*11]
        print(sub_bin_str)
        word_index = int(sub_bin_str, 2)
        word = ENGLISH_WORDLIST[word_index]
        mnemonic.append(word)

    return mnemonic


