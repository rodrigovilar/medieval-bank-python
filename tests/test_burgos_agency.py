import unittest

from burgos_agency import BurgosAgency

class TestBurgosAgency(unittest.TestCase):

    def test_initialConfig(self):
        BurgosAgency.setName("Burgosland")
        self.assertEqual("Burgosland", BurgosAgency.getName())
        BurgosAgency.setManager("Joseph")
        self.assertEqual("Joseph", BurgosAgency.getManager())

if __name__ == '__main__':
    unittest.main()
    
