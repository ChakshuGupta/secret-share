import unittest
import random
import shamir39
from shamir39.shamir_shares import generate, split_shares, combine_shares
from wordlist.wordlist_english import ENGLISH_WORDLIST
from werkzeug.exceptions import BadRequest


class TestShamirSharingMethods(unittest.TestCase):

    def test_generate(self):
        mnemonics = generate(24)
        mnemonics = mnemonics.split(" ")
        mnemonics_length = len(mnemonics)
        self.assertEqual(mnemonics_length, 24)
        for word in mnemonics:
                self.assertTrue(word in ENGLISH_WORDLIST)
    

    def test_split_shares(self):
        mnemonics = generate(15)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 5, 8)
        self.assertEqual(len(shamir_shares), 8)
        
        random.shuffle(shamir_shares)
        recovered_mnemonics = combine_shares(shamir_shares[:5])
        self.assertEqual(recovered_mnemonics, mnemonics)


    def test_recovery(self):
        mnemonics = generate(18)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 7, 10)
        self.assertEqual(len(shamir_shares), 10)
        self.assertRaises(BadRequest, combine_shares, shamir_shares[:6])



if __name__ == '__main__':
    unittest.main()