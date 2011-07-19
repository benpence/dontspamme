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

    def test_first(self):
        first = dontspamme.util.first

        expected_results = (
            (
                (('x', 'y', 'z'), lambda x: x == 'z'),
                'z'
            ),(
                ({'a': 1, 'b': 2}, lambda x: x == 'a'),
                'a'
            ),(
                ((1, 2, 3), lambda x: x == 4),
                None
            )
        )

        for test_set in expected_results:
            self.assertEqual(
                first(*test_set[0]),
                test_set[1]
            )

    def test_make_get_arguments(self):
        expected_results = (
            ({'x':'y', 'a': 3}, ('?x=y&a=3', '?a=3&x=y')),
            ({}, ('',)),
        )
        
        for kwargs, expected_result in expected_results:
            self.assertTrue(
                dontspamme.util.make_get_arguments(**kwargs) in expected_result
            )

    def test_EmailAddress(self):
        expected_results = (
            # Columns
            (
                'input',
                'original',
                'name',
                'email',
                'user',
                'contact',
                'domain'
            ),

            # Expected Values
            (
                '"Ben Pence" <ben@pence.com>',
                '"Ben Pence" <ben@pence.com>',
                'Ben Pence',
                'ben@pence.com',
                'ben',
                '',
                'pence.com'
            ),(
                '"Ben Pence" <ben@pence.com>',
                '"Ben Pence" <ben@pence.com>',
                'Ben Pence', 'ben@pence.com',
                'ben',
                '',
                'pence.com'
            ),(
                'ben@pence.com',
                'ben@pence.com',
                '',
                'ben@pence.com',
                'ben',
                '',
                'pence.com'
            ),(
                '"Ben Pence <ben@doo.doc>" <ben@pence.com>',
                '"Ben Pence <ben@doo.doc>" <ben@pence.com>',
                'Ben Pence <ben@doo.doc>',
                'ben@pence.com',
                'ben',
                '',
                'pence.com'
            ),(
                '"Ben Pence <ben+aa@doo.doc>" <ben+bb@pence.com>',
                '"Ben Pence <ben+aa@doo.doc>" <ben+bb@pence.com>',
                'Ben Pence <ben+aa@doo.doc>',
                'ben+bb@pence.com',
                'ben',
                'bb',
                'pence.com'
            ),(
                '    "Ben   Pence   "   <ben@pence.com   ',
                '"Ben Pence " <ben@pence.com',
                'Ben Pence',
                'ben@pence.com',
                'ben',
                '',
                'pence.com'
            )
        )

        for test_set in expected_results[1:]:
            address = dontspamme.util.EmailAddress(test_set[0])

            for i, property in enumerate(expected_results[0][1:]):
                self.assertEqual(
                    address.__getattribute__(property),
                    test_set[i + 1]
                )

if __name__ == '__main__':
    unittest.main()