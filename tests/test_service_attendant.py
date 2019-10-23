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

    def t02_create_attendee_without_name(self):
        attendee = Attendee()
        try:
            service.create(attendee)
            self.fail("Accepted attendee without name")
        except MedievalBankException as e:
            self.assertEquals("Name is mandatory", e.message)

    def t03_attendee_name_duplicated(self):
        attendee = Attendee()
        attendee.name = "Ana"
        service.create(attendee)

        aux_attendee = Attendee()
        aux_attendee.name = "Ana"
        try:
            service.create(aux_attendee)
            self.fail("Created attendee with existent name")
        except MedievalBankException as e:
            self.assertEquals("Name already exists", e.message)


if __name__ == '__main__':
    unittest.main()

