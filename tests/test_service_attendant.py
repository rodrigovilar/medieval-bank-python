import unittest
from datetime import datetime
from services.service_attendant import AttendeeService
from .helpers import TestAttendeeServiceHelper as helper
from persistence.models import Attendee


class TestAttendeeService(unittest.TestCase):
    service = AttendeeService()
    EX_NAME = "A Name"
    EX_EMAIL = "asd@asd.com"

    def test01_create_attendee(self):
        created_attendee = helper.create_attendee(self.service, self.EX_NAME)

        helper.validate_attendee_creation(self, self.service, created_attendee)

        searched_attendee = self.service.get_one(created_attendee.id)
        self.assertEquals(created_attendee, searched_attendee)

    def test02_create_attendee_without_name(self):
        fail_message = "Test failed because the system accepted to create an attendee without name"
        expected_exception_message = "Name is mandatory"
        attendee = Attendee()
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

    def test03_attendee_name_duplicated(self):
        fail_message = "Test failed because the system accepted to create an attendee with an already existent name"
        expected_exception_message = "Attendee name cannot be duplicated"
        helper.create_attendee(self.service, self.EX_NAME)
        attendee2 = helper.create_attendee(self.service, self.EX_NAME)
        helper.try_create_attendee_with_error(self, self.service, attendee2, fail_message, expected_exception_message)

    def test04_create_attendee_with_automatic_fields(self):
        attendee = Attendee()
        attendee.name = self.EX_NAME
        attendee.id = 123
        fail_message = "Test failed because the system accepted to create attendee with id already set"
        expected_exception_message = "Attendee id cannot be set"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

        attendee2 = Attendee()
        attendee2.name = self.EX_NAME
        attendee2.creation_date = datetime.now()
        fail_message = "Test failed because the system accepted to create attendee with creation date already set"
        expected_exception_message = "Attendee creation date cannot be set"
        helper.try_create_attendee_with_error(self, self.service, attendee2, fail_message, expected_exception_message)

    def test05_create_attendee_with_invalid_regex(self):
        attendee = Attendee()
        attendee.name = self.EX_NAME
        attendee.email = "aaa.asdasd#"

        fail_message = "Test failed because the system accepted to create attendee with invalid e-mail"
        expected_exception_message = "Attendee e-mail format is invalid"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

        attendee.email = "asdsad@@email.com"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

        attendee.email = "asdsad#email.com"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

        attendee.email = "asdsad@email"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

    def test06_update_all_editable_fields(self):
        new_email = "new@mail.com"
        new_name = "Other Name"

        attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL)
        attendee.name = new_name
        attendee.email = new_email

        updated_attendee = self.service.update(attendee)
        helper.validate_attendee_creation(self, new_name, updated_attendee, new_email)
        self.assertEquals(updated_attendee.id, attendee.id)
        self.assertEquals(updated_attendee.creation_date, attendee.creation_date)

        searched_attendee = self.service.get_one(updated_attendee.id)
        self.assertEquals(updated_attendee, searched_attendee)


if __name__ == '__main__':
    unittest.main()

