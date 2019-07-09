import sys
import os
import unittest
from os import path

sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), "."))


class BaseTest(unittest.TestCase):

    def test_ifequal(self):
        self.assertEqual(1, 1)


