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
        created_attendee1 = self.helper.create_attendee("A1")
        created_attendee2 = self.helper.create_attendee("A2")
        created_attendee3 = self.helper.create_attendee("A3")

        attendee_list = self.service.get_all()

        self.assertEquals(3, len(attendee_list))
        self.assertEquals(attendee1, attendee_list[0])
        self.assertEquals(attendee2, attendee_list[1])
        self.assertEquals(attendee3, attendee_list[2])

        return








if __name__ == '__main__':
    unittest.main()

