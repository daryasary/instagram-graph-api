import unittest

import graph_api


class FirstTest(unittest.TestCase):
    def test_package_name(self):
        self.assertEqual(graph_api.name, 'graph_api')
