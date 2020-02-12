from persistence.models import Attendee
from persistence.models import Demand
from errors.exceptions import MedievalBankException


class TestAttendeeServiceHelper:
    tester = None
    service = None

    def __init__(self, tester, service):
        self.tester = tester
        self.service = service

    ######################### DEMAND #############################
    def create_demand(self, name):
        demand = Demand()
        demand.name = name
        return self.service.create(demand)

    def validate_demand_creation(self, name, created_demand):
        self.tester.assertIsNotNone(created_demand.id)
        self.tester.assertIsNotNone(created_demand.creation_date)
        self.tester.assertEquals(name, created_demand.name)

    def try_create_demand_with_error(self, demand, fail_message, expected_exception_message):
        try:
            self.service.create(demand)
            self.tester.fail(fail_message)
        except MedievalBankException as e:
            self.tester.assertEquals(expected_exception_message, e.message)

    def try_update_demand_with_error(self, demand, fail_message, expected_exception_message):
        try:
            self.service.update(demand)
            self.tester.fail(fail_message)
        except MedievalBankException as e:
            self.tester.assertEquals(expected_exception_message, e.message)

    def try_delete_demand_with_error(self, demand, fail_message, expected_exception_message):
        try:
            self.service.delete(demand)
            self.tester.fail(fail_message)
        except MedievalBankException as e:
            self.tester.assertEquals(expected_exception_message, e.message)

    ######################## ATENDEE #######################

    def create_attendee(self, name, email=None, ssn=None):
        attendee = Attendee()
        attendee.name = name
        attendee.email = email
        attendee.ssn = ssn
        return self.service.create(attendee)

    def validate_attendee_creation(self, name, created_attendee, email=None):
        self.tester.assertIsNotNone(created_attendee.id)
        self.tester.assertIsNotNone(created_attendee.creation_date)
        self.tester.assertEquals(name, created_attendee.name)
        self.tester.assertEquals(email, created_attendee.email)

    def try_create_attendee_with_error(self, attendee, fail_message, expected_exception_message):
        try:
            self.service.create(attendee)
            self.tester.fail(fail_message)
        except MedievalBankException as e:
            self.tester.assertEquals(expected_exception_message, e.message)

    def try_update_attendee_with_error(self, attendee, fail_message, expected_exception_message):
        try:
            self.service.update(attendee)
            self.tester.fail(fail_message)
        except MedievalBankException as e:
            self.tester.assertEquals(expected_exception_message, e.message)

    def try_get_one_attendee_with_error(self, attendee_id, fail_message, expected_exception_message):
        try:
            self.service.get_one(attendee_id)
            self.tester.fail(fail_message)
        except MedievalBankException as e:
            self.tester.assertEquals(expected_exception_message, e.message)

    def try_delete_attendee_with_error(self, attendee, fail_message, expected_exception_message):
        try:
            self.service.delete(attendee)
            self.tester.fail(fail_message)
        except MedievalBankException as e:
            self.tester.assertEquals(expected_exception_message, e.message)
