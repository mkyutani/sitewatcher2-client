from argparse import Namespace
import unittest

from sw2.env import Environment

from sw2.directory.list import sw2_directory_list

class DirectoryTest(unittest.TestCase):
    """
    Category: directory.
    """

    def test_directory_list(self):
        """
        List directories.
        """
        args = {
            'category': 'directory',
            'method': 'list',
            'name': None,
            'delimiter': [' '],
            'json': False,
            'strict': False,
            'sort': False
        }
        env = Environment()
        self.assertEqual(sw2_directory_list(Namespace(**args), env), 0)

if __name__ == '__main__':
    unittest.main()
