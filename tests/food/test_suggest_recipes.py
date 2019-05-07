import unittest
import yoda
from click.testing import CliRunner


class TestSuggestRecipes(unittest.TestCase):
    """
    Test for the following commands:

        | Module: food
        | command: suggest_recipes
    """

    def __init__(self, methodName="runTest"):
        super(TestSuggestRecipes, self).__init__()
        self.runner = CliRunner()

    def runTest(self):
        # Test Recipe Suggestion
        result = self.runner.invoke(yoda.cli, ["food", "suggest_recipes"])
        self.assertIsNone(result.exception)
