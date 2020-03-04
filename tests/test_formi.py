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

        self.assertEqual(result, expected)

    def test_count_inputTextEdit_content(self):

        text = """the
            quick
            little
            brown
            fox
            jumps
            over
            the
            lazy
            dog."""

        result = formi.count_input(text)
        expected = 10

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
