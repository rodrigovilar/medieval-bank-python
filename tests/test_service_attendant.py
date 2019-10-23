import unittest
from services.service_attendant import AttendeeService
from errors.exceptions import MedievalBankException
from persistence.models import Attendee


service = AttendeeService()


class TestAttendeeService(unittest.TestCase):

    def t01_create_attendee(self):
        attendee = Attendee()
        attendee.name = "Layla"
        created_attendee = service.create(attendee)

        self.assertIsNotNone(created_attendee.id)
        self.assertIsNotNone(created_attendee.creation_date)
        self.assertEquals(attendee.name, created_attendee.name)

        searched_attendee = service.get_one(created_attendee.id)
        self.assertEquals(created_attendee, searched_attendee)


if __name__ == '__main__':
    unittest.main()

