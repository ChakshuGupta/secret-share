import binascii
import enum
import math
import string
import struct

from flask import abort
from mnemonic import Mnemonic
from utilitybelt import base58_chars, change_charset
from wordlist import WORDLIST
from pyseltongue import SecretSharer, BitcoinToB58SecretSharer

VERSION = "shamir-share-v1"
BITS = 8
STRENGTH_WORDS_MAP = {
    12 : 128,
    15 : 160,
    18 : 192,
    21 : 224,
    24 : 256
}

class Encoding(enum.Enum):
    BIP39 = 1
    BASE58 = 2



def generate(number_of_words, language="english"):
    """
    Generate a new set of mnemonic words, given the number of words

    @param number_of_words

    @return : Set of mnemonic words
    """
    new_mnemonic = Mnemonic(language)
    strength = STRENGTH_WORDS_MAP[number_of_words]

    return(new_mnemonic.generate(strength))


def split_shares(mnemonics, m, n, encoding=Encoding.BIP39, language="english"):
    """
    Split BIP39 mnemonics into Shamir Shares

    @param mnemonic_words - BIP39 Mnemonic words
    @param m - must require number of shares
    @param n - number of shares to be created
    @param encoding - Type of encoding on the shares - BIP39 or BASE58

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

    bin_str = mnemonics_to_bin(mnemonic_words, language)
    
    hex_str = hex(int(bin_str, 2))
    hex_str = hex_str.split("x")[1] # Hex string generated starts with - 0x

    shares = list()

    if encoding == Encoding.BIP39:
        shares = get_bip39_shares(hex_str, m, n, language)
    else:
        shares = get_base58_shares(hex_str, m, n)

    return shares

    
def combine_shares(shamir_shares, encoding=Encoding.BIP39, language="english"):
    """
    Combine the shamir39 shares to get BIP39 mnemonics
    
    @param shamir_shares

    @return recovered_key: secret key recovered by combining the shamir shares
    """

    hex_shamir_shares = list()
    num_required_shares = -1
    share_index = 1

    if encoding == Encoding.BIP39 :

        for share in shamir_shares:
            words = share.split(" ")

            # Check version
            if words[0] != VERSION:
                abort(400, {'message': "Incompatible version!"})

            # Extract params from prefix
            m_bin_str = ""
            index_bin_str = ""
            param_end_index = 1
            for word in words[1:]:
                word_index = WORDLIST[language].index(word)

                if word_index < 0 :
                    error_message = "Invalid word found in the mnemonics: " + word
                    abort(400, {'message': error_message})
                
                word_bin = "{0:b}".format(word_index)
                word_bin = word_bin.rjust(11, '0')

                end_of_param = word_bin[0]
                m_bin_str = m_bin_str + word_bin[1:6]
                index_bin_str = index_bin_str + word_bin[6:11]

                param_end_index += 1
                
                if end_of_param == "0":
                    break

            # Get m and index
            m = int(m_bin_str, 2)
            index = hex(int(index_bin_str, 2)).split("x")[1]

            # Set the required number of shares
            if num_required_shares == -1:
                num_required_shares = m
                # Check if the required number of shares is met
                if len(shamir_shares) < num_required_shares:
                    abort(400, {'message': "Insufficient shares provided!"})
            
            # Check consistency of m param in all shares -
            if m != num_required_shares:
                abort(400, {'message': 'Inconsistent M parameter in the shares!'})

            bin_share = mnemonics_to_bin(words[param_end_index:], language)
            hex_share =  hex(int(bin_share, 2))
            hex_share = hex_share.split("x")[1]
            hex_share = str(index) + "-" + hex_share
            hex_shamir_shares.append(hex_share)
            share_index += 1

        recovered_key_hex = SecretSharer.recover_secret(hex_shamir_shares)
    
    else:
        recovered_key_base58 = BitcoinToB58SecretSharer.recover_secret(shamir_shares)
        recovered_key_hex = change_charset(recovered_key_base58, base58_chars, string.hexdigits[0:16])

    recovered_key_bin = bin(int(recovered_key_hex, 16)).split("b")[1]
    recovered_key = bin_to_mnemonics(recovered_key_bin, language)
    recovered_key = " ".join(recovered_key)
    
    return recovered_key


def bin_to_mnemonics(bin_str, language):
    """
    Convert binary string to mnemonics
    
    @param bin_str: Binary string

    @return list of mnemonic words
    """
    mnemonic = list()

    total_words = int(math.ceil(len(bin_str)/11))
    total_bits = total_words * 11
    bin_str = bin_str.rjust(total_bits, '0')

    for i in range(0, total_words):
        sub_bin_str = bin_str[i*11 : (i+1)*11]
        word_index = int(sub_bin_str, 2)
        word = WORDLIST[language][word_index]
        mnemonic.append(word)

    return mnemonic


def mnemonics_to_bin(mnemonic_words, language):
    """
    Convert mnemonics to binary string

    @param mnemonic words as a string

    @return binary string
    """
    bin_str = ""
    for word in mnemonic_words:
        word_index = WORDLIST[language].index(word)
        if word_index < 0:
            error_message = "Invalid word found in the mnemonics: " + word
            abort(400, {'message': error_message})
        index_bits =  "{0:b}".format(word_index)
        index_bits = index_bits.rjust(11, '0')
        bin_str += index_bits
    
    return bin_str


def params_to_bin_str(m, index):
    """
    Convert share parameters to binary string

    @param m: minimun shares required to recover the secret
    @param index: index number of the share

    @return bin_str: binary string of the parameters
    """

    m_bin = "{0:b}".format(m)
    index_bin = "{0:b}".format(index)

    # Binary string should be multiple of 5
    m_bin_final_length = math.ceil(len(m_bin) / 5) * 5
    index_bin_final_length = math.ceil(len(index_bin) / 5) * 5
    bin_final_length = max(m_bin_final_length, index_bin_final_length)

    m_bin = m_bin.rjust(bin_final_length, '0')
    index_bin = index_bin.rjust(bin_final_length, '0')

    total_words = int(len(m_bin) / 5)

    bin_str = ""
    for i in range(0, total_words):
        leading_bit = '1'
        
        if i == total_words-1:
            leading_bit = '0'

        m_bits = m_bin[i*5 : (i+1)*5]
        index_bits = index_bin[i*5 : (i+1)*5]
        bin_str += leading_bit + m_bits + index_bits

    return bin_str


def get_bip39_shares(hex_str, m, n, language):
    """

    """
    shamir_shares = SecretSharer.split_secret(hex_str, m, n)

    shamir39_shares  = list()
    for share in shamir_shares:
        mnemonic_words = list()
        share_index, share = share.split("-")        
        params_binary = params_to_bin_str(m, int(share_index, 16))
            
        share_binary = bin(int(share, 16))
        share_binary = share_binary.split("b")[1] # Binary string generated starts with - 0b
        # Every mnemonic has version as the first word.
        mnemonic_words.append(VERSION)
        mnemonic_words.extend(bin_to_mnemonics(params_binary, language))
        mnemonic_words.extend(bin_to_mnemonics(share_binary, language))

        mnemonic_string = " ".join(mnemonic_words)
        shamir39_shares.append(mnemonic_string)

    return shamir39_shares



def get_base58_shares(hex_str, m, n):
    """
    Convert the hex string to a base58 string and split it into "n" shares.
    """
    base58_str = change_charset(hex_str, string.hexdigits[0:16], base58_chars)
    shares = BitcoinToB58SecretSharer.split_secret(base58_str, m, n)

    return shares
