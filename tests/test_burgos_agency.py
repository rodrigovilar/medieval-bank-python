import unittest

from burgos_agency import AgencyService

class TestBurgosAgency(unittest.TestCase):

    def test_initialConfig(self):
        service = AgencyService()
        service = AgencyService()
        service.setName("Burgosland")
        self.assertEqual("Burgosland", service.getName())
        service.setManager("Joseph")
        self.assertEqual("Joseph", service.getManager())


if __name__ == '__main__':
    unittest.main()

