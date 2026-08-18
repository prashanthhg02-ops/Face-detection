"""Test package for Face Detection with AIML"""

import unittest


def load_tests():
    """Load all tests from this package."""
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(load_tests())
