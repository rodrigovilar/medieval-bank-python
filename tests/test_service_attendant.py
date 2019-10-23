import unittest
from services.service_attendant import AttendeeService
from errors.exceptions import MedievalBankException
from persistence.models import Attendee


class TestAttendeeService(unittest.TestCase):
    service = AttendeeService()

    def create_attendee(self, name):
        attendee = Attendee()
        attendee.name = name
        return self.service.create(attendee)

    def validate_attendee_creation(self,name, created_attendee):
        self.assertIsNotNone(created_attendee.id)
        self.assertIsNotNone(created_attendee.creation_date)
        self.assertEquals(name, created_attendee.name)

    def try_create_attendee_with_error(self, name, fail_message, expected_exception_message):
        try:
            self.create_attendee(name)
            self.fail(fail_message)
        except MedievalBankException as e:
            self.assertEquals(expected_exception_message, e.message)

    def t01_create_attendee(self):
        a_name = "A Name"
        created_attendee = self.create_attendee(a_name)

        self.validate_attendee_creation(created_attendee)

        searched_attendee = self.service.get_one(created_attendee.id)
        self.assertEquals(created_attendee, searched_attendee)

    def t02_create_attendee_without_name(self):
        fail_message = "Test failed because the system accepted to create an attendee without name"
        expected_exception_message = "Name is mandatory"
        self.try_create_attendee_with_error(None, fail_message, expected_exception_message)

    def t03_attendee_name_duplicated(self):
        a_name = "A Name"
        fail_message = "Test failed because the system accepted to create an attendee with an already existent name"
        expected_exception_message = "Attendee name cannot be duplicated"
        self.create_attendee(a_name)
        self.try_create_attendee_with_error(a_name, fail_message, expected_exception_message)


if __name__ == '__main__':
    unittest.main()

