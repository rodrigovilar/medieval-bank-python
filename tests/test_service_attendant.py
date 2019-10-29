import unittest
from datetime import datetime
from services.service_attendant import AttendeeService
from errors.exceptions import MedievalBankException
from persistence.models import Attendee


class TestAttendeeService(unittest.TestCase):
    service = AttendeeService()
    EX_NAME = "A Name"

    def create_attendee(self, name):
        attendee = Attendee()
        attendee.name = name
        return self.service.create(attendee)

    def validate_attendee_creation(self,name, created_attendee):
        self.assertIsNotNone(created_attendee.id)
        self.assertIsNotNone(created_attendee.creation_date)
        self.assertEquals(name, created_attendee.name)

    def try_create_attendee_with_error(self, attendee, fail_message, expected_exception_message):
        try:
            self.service.create(attendee)
            self.fail(fail_message)
        except MedievalBankException as e:
            self.assertEquals(expected_exception_message, e.message)

    def t01_create_attendee(self):
        created_attendee = self.create_attendee(self.EX_NAME)

        self.validate_attendee_creation(created_attendee)

        searched_attendee = self.service.get_one(created_attendee.id)
        self.assertEquals(created_attendee, searched_attendee)

    def t02_create_attendee_without_name(self):
        fail_message = "Test failed because the system accepted to create an attendee without name"
        expected_exception_message = "Name is mandatory"
        attendee = Attendee()
        self.try_create_attendee_with_error(attendee, fail_message, expected_exception_message)

    def t03_attendee_name_duplicated(self):
        fail_message = "Test failed because the system accepted to create an attendee with an already existent name"
        expected_exception_message = "Attendee name cannot be duplicated"
        self.create_attendee(self.EX_NAME)
        attendee2 = self.create_attendee(self.EX_NAME)
        self.try_create_attendee_with_error(attendee2, fail_message, expected_exception_message)

    def t04_create_attendee_with_automatic_fields(self):
        attendee = Attendee()
        attendee.name = self.EX_NAME
        attendee.id = 123
        fail_message = "Test failed because the system accepted to create attendee with id already set"
        expected_exception_message = "Attendee id cannot be set"
        self.try_create_attendee_with_error(attendee, fail_message, expected_exception_message)

        attendee2 = Attendee()
        attendee2.name = self.EX_NAME
        attendee2.creation_date = datetime.now()
        fail_message = "Test failed because the system accepted to create attendee with creation date already set"
        expected_exception_message = "Attendee creation date cannot be set"
        self.try_create_attendee_with_error(attendee2, fail_message, expected_exception_message)

    def t05_create_attendee_with_invalid_regex(self):
        attendee = Attendee()
        attendee.name = self.EX_NAME
        attendee.email = "aaa.asdasd#"

        fail_message = "Test failed because the system accepted to create attendee with invalid e-mail"
        expected_exception_message = "Attendee e-mail format is invalid"
        self.try_create_attendee_with_error(attendee, fail_message, expected_exception_message)


if __name__ == '__main__':
    unittest.main()

