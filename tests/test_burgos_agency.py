import unittest

from burgos_agency import AgencyService
from services.service_attendant import AttendeeService

class TestBurgosAgency(unittest.TestCase):

    def test_initialConfig(self):
        service = AgencyService()
        service.setName("Burgosland")
        self.assertEqual("Burgosland", service.getName())
        service.setManager("Joseph")
        self.assertEqual("Joseph", service.getManager())

    def test_three_attendees(self):
        agency_service = AgencyService()
        attendee_service = AttendeeService()
        attendee1 = self.helper.create_attendee("A1")
        attendee2 = self.helper.create_attendee("A2")
        attendee3 = self.helper.create_attendee("A3")

        self.assertEquals(agency_service.status, "Attendees: [A1, A2, A3]\nQueue: []")






if __name__ == '__main__':
    unittest.main()

