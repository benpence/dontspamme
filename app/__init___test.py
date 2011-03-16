import unittest

import __init__

class Tests(unittest.TestCase):
    
    def test_random_hash(self):
        """
        
        """
        UNIQUE_ITEMS = 100000
        HASH_LENGTH = 12
        
        uniques = set()
        
        for i in range(UNIQUE_ITEMS):
            uniques.add(
                __init__.random_hash(HASH_LENGTH)
            )
            
        self.assertEqual(
            len(uniques),
            UNIQUE_ITEMS
        )
        
    def test_email_split(self):
        tests = (
            (('hy+ho@dd.com', '+', '@'),          'ho'),
            (('ok@donkey.net', '@', ''),          'donkey.net'),
            (('doo+ee+fff@ell.com', '+', '@'),    'fff'),
            (('my+ee+ee+ff@spieys.com', '+', ''), 'ff@spieys.com'),
            (('heythere@everyone.com', '+', '@'), None),
        )
        
        for test in tests:
            arguments, expected_result = test
            
            self.assertEqual(
                __init__.email_split(*arguments),
                expected_result
            )
    
if __name__ == '__main__':
    unittest.main()