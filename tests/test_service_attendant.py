import unittest
from datetime import datetime
from services.service_attendant import AttendeeService
from .helpers import TestAttendeeServiceHelper as helper
from persistence.models import Attendee, Base, tear_down_test_db
from errors.messages import AttendeeMessages
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from persistence import test_db_path


class TestAttendeeService(unittest.TestCase):
    service = AttendeeService()
    EX_NAME = "A Name"
    EX_OTHER_NAME = "Other Name"
    EX_EMAIL = "asd@gmail.com"
    EX_SSN = "473-20-6799"
    UNKNOWN_ID = 202020

    def setUp(self):
        self.service.open_session()

    def tearDown(self):
        tear_down_test_db()
        self.service.close_session()

    def test01_create_attendee(self):
        created_attendee = helper.create_attendee(self.service, self.EX_NAME)

        helper.validate_attendee_creation(self, self.EX_NAME, created_attendee)

        searched_attendee = self.service.get_one(created_attendee.id)
        self.assertEquals(created_attendee, searched_attendee)

    def test02_create_attendee_without_name(self):
        fail_message = "Test failed because the system accepted to create an attendee without name"
        attendee = Attendee()
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message,
                                              AttendeeMessages.NON_NULLABLE_NAME)

    def test03_attendee_name_duplicated(self):
        fail_message = "Test failed because the system accepted to create an attendee with an already existent name"
        helper.create_attendee(self.service, self.EX_NAME)
        attendee2 = Attendee()
        attendee2.name = self.EX_NAME
        helper.try_create_attendee_with_error(self, self.service, attendee2, fail_message, AttendeeMessages.UNIQUE_NAME)

    def test04_create_attendee_with_automatic_fields(self):
        attendee = Attendee()
        attendee.name = self.EX_NAME
        attendee.id = 123
        fail_message = "Test failed because the system accepted to create attendee with id already set"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, AttendeeMessages.IMMUTABLE_ID)

        attendee2 = Attendee()
        attendee2.name = self.EX_NAME
        attendee2.creation_date = datetime.now()
        fail_message = "Test failed because the system accepted to create attendee with creation date already set"
        helper.try_create_attendee_with_error(self, self.service, attendee2, fail_message, AttendeeMessages.IMMUTABLE_CREATION_DATE)

    def test05_create_attendee_with_invalid_regex(self):
        attendee = Attendee()
        attendee.name = self.EX_NAME
        attendee.email = "aaa.asdasd#"

        fail_message = "Test failed because the system accepted to create attendee with invalid e-mail"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, AttendeeMessages.WRONG_FORMAT_EMAIL)

        attendee.email = "asdsad@@email.com"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, AttendeeMessages.WRONG_FORMAT_EMAIL)

        attendee.email = "asdsad#email.com"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, AttendeeMessages.WRONG_FORMAT_EMAIL)

        attendee.email = "asdsad@email"
        helper.try_create_attendee_with_error(self, self.service, attendee, fail_message, AttendeeMessages.WRONG_FORMAT_EMAIL)

    def test06_update_all_editable_fields(self):
        new_email = "new@mail.com"

        attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL)
        attendee.name = self.EX_OTHER_NAME
        attendee.email = new_email

        updated_attendee = self.service.update(attendee)
        helper.validate_attendee_creation(self, self.EX_OTHER_NAME, updated_attendee, new_email)
        self.assertEquals(updated_attendee.id, attendee.id)
        self.assertEquals(updated_attendee.creation_date, attendee.creation_date)

        searched_attendee = self.service.get_one(updated_attendee.id)
        self.assertEquals(updated_attendee, searched_attendee)

    def test07_update_attendee_with_immutable_fields(self):
        attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN)
        attendee.ssn = "385-42-9044"

        fail_message = "Test failed because the system accepted to update attendee with a new ssn"
        expected_exception_message = "Attendee SSN is immutable"
        helper.try_update_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

    def test08_update_attendee_with_unknown_id(self):
        attendee_with_unknown_id = Attendee()

        attendee_with_unknown_id.id = self.UNKNOWN_ID

        fail_message = "Test failed because the system accepted to update attendee with an unknown ID"
        expected_exception_message = "Attendee ID not found: " + str(self.UNKNOWN_ID)
        helper.try_update_attendee_with_error(self, self.service, attendee_with_unknown_id,
                                              fail_message, expected_exception_message)

        created_attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN)
        created_attendee.id = self.UNKNOWN_ID
        helper.try_update_attendee_with_error(self, self.service, attendee_with_unknown_id,
                                              fail_message, expected_exception_message)

    def test09_update_attendee_without_name(self):
        fail_message = "Test failed because the system accepted to update an attendee without name"
        expected_exception_message = "Name is mandatory"
        attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN)
        helper.try_update_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

    def test10_update_attendee_name_duplicated(self):
        helper.create_attendee(self.service, self.EX_NAME)
        attendee2 = helper.create_attendee(self.service, self.EX_OTHER_NAME)
        attendee2.name = self.EX_NAME

        fail_message = "Test failed because the system accepted to update an attendee with an already existent name"
        expected_exception_message = "Attendee name cannot be duplicated"
        helper.try_update_attendee_with_error(self, self.service, attendee2, fail_message, expected_exception_message)
        
    def test11_update_attendee_WindthAutomaticField(self):
        created_attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)
        sleep(0.01)
        created_attendee.creation_date = datetime.now()

        fail_message = "Test failed because the system accepted to update an attendee with an already existent name"
        expected_exception_message = "Attendee name cannot be duplicated"
        helper.try_update_attendee_with_error(self, self.service, created_attendee, fail_message,
                                              expected_exception_message)

    def test12_update_attendee_with_invalid_email(self):
        attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)

        fail_message = "Test failed because the system accepted to update attendee with invalid e-mail format"
        expected_exception_message = "Attendee e-mail format is invalid"

        attendee.email = "sdsdfa.sds#"
        helper.try_update_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

        attendee.email = "sdsdfa@@gmail.com"
        helper.try_update_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)

        attendee.email = "sdsdfa#gmail.com"
        helper.try_update_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)
      
        attendee.email = "sdsdfa@gmail"
        helper.try_update_attendee_with_error(self, self.service, attendee, fail_message, expected_exception_message)
    
    def test13_delete_attendee(self):
        created_attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)

        self.service.delete(created_attendee)

        fail_message = "Test failed because the system returned an unknown attendee"
        helper.try_get_one_attendee_with_error(self, self.service, created_attendee.id, fail_message,
                                               AttendeeMessages(created_attendee.id).UNKNOWN_ID)

    def test14_delete_unknown_attendee(self):
        created_attendee = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)
        created_attendee.id = self.UNKNOWN_ID

        self.service.delete(created_attendee)
        fail_message = "Test failed because the system accepted to delete attendee with an unknown id"

        helper.try_delete_attendee_with_error(self, self.service, created_attendee, fail_message,
                                              AttendeeMessages(created_attendee.id).UNKNOWN_ID)

        fail_message = "Test failed because the system accepted to delete a null attendee"
        helper.try_delete_attendee_with_error(self, self.service, None, fail_message, AttendeeMessages.NULL_ATTENDEE)

    def test15_three_attendees(self):
        attendee1 = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL)
        attendee2 = helper.create_attendee(self.service, self.EX_OTHER_NAME)
        attendee3 = helper.create_attendee(self.service, "Third Name")

        attendee_list = self.service.get_all()
        self.assertEquals(3, attendee_list.size())
        self.assertEquals(attendee1,attendee_list[0])
        self.assertEquals(attendee2,attendee_list[1])
        self.assertEquals(attendee3,attendee_list[2])

    def test16_filter_attendees(self):
        attendee1 = helper.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL)
        attendee2 = helper.create_attendee(self.service, self.EX_OTHER_NAME)
        attendee3 = helper.create_attendee(self.service, "Third Name")

        attendee_list = self.service.find_by_name("Name")
        self.assertEquals(1, attendee_list.size())
        self.assertEquals(attendee3, attendee_list[0])

        attendee_list = self.service.find_by_name("Name")
        self.assertEquals(3, attendee_list.size())
        self.assertEquals(attendee1, attendee_list[0])
        self.assertEquals(attendee2, attendee_list[1])
        self.assertEquals(attendee3, attendee_list[2])

        attendee_list = self.service.find_by_name("Jhon")
        self.assertEquals(0,attendee_list.size)


if __name__ == '__main__':
    unittest.main()

