import unittest
import json
from poe.public_stash_tabs import PST


class PSTTextCase(unittest.TestCase):
	def test_create_public_stash_tabs(self):
		tab = PST()
		self.assertIsInstance(tab.stashes, list)  # JsonArray


if __name__ == '__main__':
	unittest.main()
