import unittest

import dontspamme.util

class TestSequenceFunctions(unittest.TestCase):
    NUMBER_OF_TESTS = 100000

    def setUp(self):
        pass

    def test_generate_random_string(self):
        uniques = set()

        for i in xrange(self.NUMBER_OF_TESTS):
            uniques.add(dontspamme.util.generate_random_string())

        self.assertEqual(len(uniques), self.NUMBER_OF_TESTS)

    def test_EmailAddress(self):
        expected_results = (
            # Columns
            ('original', 'name', 'email', 'user', 'contact', 'domain'),

            # Expected Values
            ('"Ben Pence" <ben@pence.com>', 'Ben Pence', 'ben@pence.com', 'ben', None, 'pence.com'),
            ('"Ben Pence" <ben@pence.com>', 'Ben Pence', 'ben@pence.com', 'ben', None, 'pence.com'),
            ('ben@pence.com', None, 'ben@pence.com', 'ben', None, 'pence.com'),
            ('"Ben Pence <ben@doo.doc>" <ben@pence.com>', 'Ben Pence <ben@doo.doc>', 'ben@pence.com', 'ben', None, 'pence.com'),
            ('"Ben Pence <ben+aa@doo.doc>" <ben+bb@pence.com>', 'Ben Pence <ben+aa@doo.doc>', 'ben+bb@pence.com', 'ben', 'bb', 'pence.com'),
        )

        for test_set in expected_results[1:]:
            address = dontspamme.util.EmailAddress(test_set[0])

            for i, property in enumerate(expected_results[0]):
                self.assertEqual(
                    address.__getattribute__(property),
                    test_set[i]
                )

if __name__ == '__main__':
    unittest.main()
