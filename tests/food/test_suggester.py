import unittest
import sys

from yoda import food


class TestSuggester(unittest.TestCase):
    """
    Test for the suggerter function
    """

    def runTest(self):
        # Test suggester
        self.assertRaises(TypeError, food.suggester, 1)
        self.assertRaises(ValueError, food.suggester, 'meels')

