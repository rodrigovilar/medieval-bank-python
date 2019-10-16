import unittest

from burgos_bank import BurgosBank

class TestBurgosBank(unittest.TestCase):

    def test_initialConfig(self):
        BurgosBank.setName("Burgosland")
        self.assertEqual("Burgosland", BurgosBank.getName())
        BurgosBank.setManager("Joseph")
        self.assertEqual("Joseph", BurgosBank.getManager())

if __name__ == '__main__':
    unittest.main()
    