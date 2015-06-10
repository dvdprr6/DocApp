import os
import sys
import unittest

from colour_runner.runner import ColourTextTestRunner

def get_all_tests():
    loader = unittest.TestLoader()
    all_tests = unittest.TestLoader().discover('tests', pattern='*.py')
    return all_tests

def run_all_tests():
    all_tests = get_all_tests()
    try:
        runner = ColourTextTestRunner(verbosity=2)
    except:
        runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(all_tests)
    return result

'''
Usage: python tests/doc_tests.py
'''
if __name__ == '__main__':
    results = run_all_tests()