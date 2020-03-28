import binascii
import math
import struct

from flask import abort

from wordlist.wordlist_english import ENGLISH_WORDLIST
from pyseltongue import SecretSharer

VERSION = "shamir-share-v1"

def split_shares(mnemonics, m, n):
    """
    Split BIP39 mnemonics into Shamir Shares

    @param mnemonic_words - BIP39 Mnemonic words
    @param m - must require number of shares
    @param n - number of shares to be created

    @return shamir39_shares 
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

    bin_str = mnemonics_to_bin(mnemonic_words)
    
    hex_str = hex(int(bin_str, 2))
    hex_str = hex_str.split("x")[1] # Hex string generated starts with - 0x

    shamir_shares = SecretSharer.split_secret(hex_str, m, n)
    print(shamir_shares)

    shamir39_shares  = list()
    for share in shamir_shares:
        shamir39_shares.append(shares_to_shamir39_mnemonics(share))

    return shamir39_shares


def combine_shares(shamir_shares):
    """
    Combine the shamir39 shares to get BIP39 mnemonics
    
    @param shamir_shares

    @return recovered_key: secret key recovered by combining the shamir shares
    """

    hex_shamir_shares = list()
    # num_required_shares = -1
    share_index = 1

    for share in shamir_shares:
        words = share.split(" ")

        if words[0] != VERSION:
            abort(400, {'message': "Incompatible version!"})

        bin_share = mnemonics_to_bin(words[1:])
        hex_share =  hex(int(bin_share, 2))
        hex_share = hex_share.split("x")[1]
        hex_share = str(share_index) + "-" + hex_share
        hex_shamir_shares.append(hex_share)
        share_index += 1
    
    print(hex_shamir_shares)
    recovered_key_hex = SecretSharer.recover_secret(hex_shamir_shares)
    recovered_key_bin = bin(int(recovered_key_hex, 16)).split("b")[1]
    recovered_key = bin_to_mnemonics(recovered_key_bin)
    recovered_key = " ".join(recovered_key)
    
    return recovered_key


def shares_to_shamir39_mnemonics(shamir_share):
    """
    Convert the shamir share to shamir39 mnemonic words

    @param shamir_share - Shamir share in hex form

    @return mnemonic_string: corresponding shamir39 mnemonic words
    """
    share = shamir_share.split("-")[1]

    share_binary = bin(int(share, 16))
    share_binary = share_binary.split("b")[1] # Binary string generated starts with - 0b
    mnemonic_words = list()
    # Every mnemonic has version as the first word.
    mnemonic_words.append(VERSION)
    mnemonic_words.extend(bin_to_mnemonics(share_binary))

    mnemonic_string = " ".join(mnemonic_words)
    return mnemonic_string


def bin_to_mnemonics(bin_str):
    """
    Convert binary string to mnemonics
    
    @param bin_str: Binary string

    @return list of mnemonic words
    """
    mnemonic = list()

    total_words = int(math.ceil(len(bin_str)/11))
    total_bits = total_words * 11
    print(total_words, total_bits)
    bin_str = bin_str.rjust(total_bits, '0')

    for i in range(0, total_words):
        sub_bin_str = bin_str[i*11 : (i+1)*11]
        word_index = int(sub_bin_str, 2)
        word = ENGLISH_WORDLIST[word_index]
        mnemonic.append(word)

    return mnemonic


def mnemonics_to_bin(mnemonic_words):
    """
    Convert mnemonics to binary string

    @param mnemonic words as a string

    @return binary string
    """
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
    
    return bin_str


