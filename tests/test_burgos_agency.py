import unittest

from burgos_agency_Renato import AgencyService

class TestBurgosAgency(unittest.TestCase):

    agency = AgencyService

    def test_initialConfig(self):
        service = AgencyService()
        service = AgencyService()
        service.setName("Burgosland")
        self.assertEqual("Burgosland", service.getName())
        service.setManager("Joseph")
        self.assertEqual("Joseph", service.getManager())

    def emptyStatusAndQueue(self):
        self.agency.getstatus()
        self.agency.getqueue()


if __name__ == '__main__':
    unittest.main()

