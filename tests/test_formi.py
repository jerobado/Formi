import unittest
from src.core import formi


class FormiCoreTestCase(unittest.TestCase):
    """ Test formi.py core functions """

    def test_join_string_function(self):

        result = formi.join_string('the\nquick')
        expected = 'the, quick'

        self.assertEqual(result, expected)

    def test_expand_string_function(self):

        result = formi.expand_string('the quick')
        expected = 'the\nquick'
        print(result)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
