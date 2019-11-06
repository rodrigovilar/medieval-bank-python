from persistence.models import Attendee
from errors.exceptions import MedievalBankException


class TestAttendeeServiceHelper:

    @staticmethod
    def create_attendee(service, name, email=None, ssn=None):
        attendee = Attendee()
        attendee.name = name
        attendee.email = email
        attendee.ssn = ssn
        return service.create(attendee)

    @staticmethod
    def validate_attendee_creation(tester, name, created_attendee, email=None):
        tester.assertIsNotNone(created_attendee.id)
        tester.assertIsNotNone(created_attendee.creation_date)
        tester.assertEquals(name, created_attendee.name)
        tester.assertEquals(email, created_attendee.email)

    @staticmethod
    def try_create_attendee_with_error(tester, service, attendee, fail_message, expected_exception_message):
        try:
            service.create(attendee)
            tester.fail(fail_message)
        except MedievalBankException as e:
            tester.assertEquals(expected_exception_message, e.message)

    @staticmethod
    def try_update_attendee_with_error(tester, service, attendee, fail_message, expected_exception_message):
        try:
            service.update(attendee)
            tester.fail(fail_message)
        except MedievalBankException as e:
            tester.assertEquals(expected_exception_message, e.message)
    
    @staticmethod
    def try_get_one_attendee_with_error(tester, service, attendee_id, fail_message, expected_exception_message):
        try:
            service.update(attendee_id)
            tester.fail(fail_message)
        except MedievalBankException as e:
            tester.assertEquals(expected_exception_message, e.message)

    @staticmethod
    def try_delete_attendee_with_error(tester, service, attendee, fail_message, expected_exception_message):
        try:
            service.update(attendee)
            tester.fail(fail_message)
        except MedievalBankException as e:
            tester.assertEquals(expected_exception_message, e.message)
