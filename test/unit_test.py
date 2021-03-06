import unittest
import random
import shamir39
from shamir39.shamir_shares import generate, split_shares, combine_shares, Encoding
from wordlist import WORDLIST
from werkzeug.exceptions import BadRequest


class TestShamirSharingMethods(unittest.TestCase):

    def test_generate(self):
        mnemonics = generate(24)
        mnemonics = mnemonics.split(" ")
        mnemonics_length = len(mnemonics)
        self.assertEqual(mnemonics_length, 24)
        for word in mnemonics:
                self.assertTrue(word in WORDLIST["english"])

    
    def test_generate_french(self):
        language = "french"
        mnemonics = generate(24, language)
        mnemonics = mnemonics.split(" ")
        mnemonics_length = len(mnemonics)
        self.assertEqual(mnemonics_length, 24)
        for word in mnemonics:
                self.assertTrue(word in WORDLIST[language])


    def test_generate_italian(self):
        language = "italian"
        mnemonics = generate(24, language)
        mnemonics = mnemonics.split(" ")
        mnemonics_length = len(mnemonics)
        self.assertEqual(mnemonics_length, 24)
        for word in mnemonics:
                self.assertTrue(word in WORDLIST[language])


    def test_split_shares(self):
        mnemonics = generate(15)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 5, 8)
        self.assertEqual(len(shamir_shares), 8)
        
        random.shuffle(shamir_shares)
        recovered_mnemonics = combine_shares(shamir_shares[:5])
        self.assertEqual(recovered_mnemonics, mnemonics)


    def test_split_shares_french(self):
        language = "french"
        mnemonics = generate(15, language)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 5, 8, language=language)
        self.assertEqual(len(shamir_shares), 8)
        
        random.shuffle(shamir_shares)
        recovered_mnemonics = combine_shares(shamir_shares[:5], language=language)
        self.assertEqual(recovered_mnemonics, mnemonics)


    def test_split_shares_italian(self):
        language = "italian"
        mnemonics = generate(15, language)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 5, 8, language=language)
        self.assertEqual(len(shamir_shares), 8)
        
        random.shuffle(shamir_shares)
        recovered_mnemonics = combine_shares(shamir_shares[:5], language=language)
        self.assertEqual(recovered_mnemonics, mnemonics)


    def test_split_shares_base58(self):
        mnemonics = generate(15)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 5, 8, encoding=Encoding.BASE58)
        self.assertEqual(len(shamir_shares), 8)
        random.shuffle(shamir_shares)
        recovered_mnemonics = combine_shares(shamir_shares[:5], encoding=Encoding.BASE58)
        self.assertEqual(recovered_mnemonics, mnemonics)


    def test_recovery(self):
        mnemonics = generate(18)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 7, 10)
        self.assertEqual(len(shamir_shares), 10)
        recovered_mnemonics = combine_shares(shamir_shares[:9])
        self.assertEqual(recovered_mnemonics, mnemonics)

        self.assertRaises(BadRequest, combine_shares, shamir_shares[:6])

    def test_recovery_base58(self):
        mnemonics = generate(18)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 7, 10, encoding=Encoding.BASE58)
        self.assertEqual(len(shamir_shares), 10)
        recovered_mnemonics = combine_shares(shamir_shares[:9], encoding=Encoding.BASE58)
        self.assertEqual(recovered_mnemonics, mnemonics)
        #Verify not equal values with less shares
        recovered_incorrect = combine_shares(shamir_shares[:6], encoding=Encoding.BASE58)
        self.assertNotEqual(mnemonics, recovered_incorrect)

    
    def test_base58_italian(self):
        language = "italian"
        mnemonics = generate(15,language=language)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 5, 8, encoding=Encoding.BASE58, language=language)
        self.assertEqual(len(shamir_shares), 8)
        random.shuffle(shamir_shares)
        recovered_mnemonics = combine_shares(shamir_shares[:5], encoding=Encoding.BASE58, language=language)
        self.assertEqual(recovered_mnemonics, mnemonics)
        
        recovered_incorrect = combine_shares(shamir_shares[:3], encoding=Encoding.BASE58, language=language)
        self.assertNotEqual(mnemonics, recovered_incorrect)

        
    def test_base58_french(self):
        language = "french"
        mnemonics = generate(24,language=language)
        # Get 5 of 8 split
        shamir_shares = split_shares(mnemonics, 10, 15, encoding=Encoding.BASE58, language=language)
        self.assertEqual(len(shamir_shares), 15)
        random.shuffle(shamir_shares)
        recovered_mnemonics = combine_shares(shamir_shares[:10], encoding=Encoding.BASE58, language=language)
        self.assertEqual(recovered_mnemonics, mnemonics)
        
        recovered_incorrect = combine_shares(shamir_shares[:6], encoding=Encoding.BASE58, language=language)
        self.assertNotEqual(mnemonics, recovered_incorrect)




if __name__ == '__main__':
    unittest.main()