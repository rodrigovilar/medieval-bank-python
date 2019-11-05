import unittest
from datetime import datetime
from services.service_attendant import AttendeeService
from .helpers import TestAttendeeServiceHelper as helper
from persistence.models import Attendee
from time import sleep

class TestAttendeeService(unittest.TestCase):
    service = AttendeeService()
    EX_NAME = "A Name"
    EX_OTHER_NAME = "Other Name"
    EX_EMAIL = "asd@asd.com"
    EX_SSN = "473-20-6799"
    UNKNOWN_ID = 202020

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
        created_attendee = help.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)
        sleep(0.01)
        created_attendee.creation_date = datetime.now()

        fail_message = "Test failed because the system accepted to update an attendee with an already existent name"
        expected_exception_message = "Attendee name cannot be duplicated"
        helper.try_update_attendee_with_error(self, self.service, fail_message, expected_exception_message)

    def test12_update_atendee_WithInvalid_Email(self):
        created_attendee = help.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)

        fail_message = "Test failed because the system accepted to update atendee with invalid e-mail format"
        expected_exception_message = "Attendee e-mail format is invalid"
        helper.try_update_attendee_with_error(self, self.service, fail_message, expected_exception_message)

        attendee.email = self.EX_EMAIL("sdsdfa.sds#")
        helper.try_update_attendee_with_error(self, self.service, fail_message, expected_exception_message)

        attendee.email = self.EX_EMAIL("sdsdfa@@gmail.com")
        helper.try_update_attendee_with_error(self, self.service, fail_message, expected_exception_message)

        attendee.email = self.EX_EMAIL("sdsdfa#gmail.com")
        helper.try_update_attendee_with_error(self, self.service, fail_message, expected_exception_message)
      
        attendee.email = self.EX_EMAIL("sdsdfa@gmail")
        helper.try_update_attendee_with_error(self, self.service, fail_message, expected_exception_message)
    
    def test13_deleteAttendee(self):
        created_attendee = help.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)

        self.service.delete(created_attendee)
        fail_message = "Test failed because the system returned an unknown attendee"
        expected_exception_message = "Unknown Atendee id: " + self.attendee.id

        helper.try_get_one_attendee_with_error(self, self.service, fail_message, expected_exception_message)

    def test14_delete_unknown_attendee(self):
        created_attendee = help.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL, self.EX_SSN,)

        attendee_delete_unknown.attendee.id = Attendee()
        attendee_delete_unknown.attendee.id.id= self.UNKNOWN_ID

        self.service.delete(created_attendee)
        fail_message = "Test failed because the system accepted to delete atendee with an unknown id"
        expected_exception_message = "Atendee id not found: " + self.attendee.id

        helper.try_delete_attendee_with_error(self, self.service, fail_message, expected_exception_message)

        fail_message = "Test failed because the system accepted to delete a null atendee"
        expected_exception_message = "Null attendee"
        helper.try_delete_attendee_with_error(self, self.service, fail_message, expected_exception_message)

    def test15_three_attendees(self):
        attendee1 =  help.create_attendee(self.service, self.EX_NAME, self.EX_EMAIL)
        attendee2 = help.create_attendee(self.service, self.EX_OTHER_NAME)
        attendee3 = help.create_attendee(self.service, "Thrid Name")

        lista_attendees = self.service.get_all()
        self.assertEquals(3, lista_attendees.size())
        self.assertEquals(attendee1,lista_attendees[0])
        self.assertEquals(attendee2,lista_attendees[1])
        self.assertEquals(attendee3,lista_attendees[2])
        

if __name__ == '__main__':
    unittest.main()

