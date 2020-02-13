import unittest

from services.service_agency import AgencyService

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

class TestServiceAgency(unittest.TestCase):

    service_atendee = AttendeeService()
    service_agency = AgencyService(service_atendee)

    EX_NAME = "A Name"
    EX_OTHER_NAME = "Other Name"
    EX_EMAIL = "asd@gmail.com"
    EX_SSN = "473-20-6799"
    UNKNOWN_ID = 202020


    def setUp(self):
        self.service_atendee.open_session()

    def tearDown(self):
        tear_down_test_db()
        self.service_atendee.close_session()

    def test14_agency_status(self):
        result = self.service_agency.getStatus() # Criar meth getStatus
        self.assertEquals(result, "Atendees: []\n Queue: []")

    def test17_return_one(self):
        service_atendee = self.service_atendee
        service_atendee.helper.create_attendee("A1")
        self.assertEquals(self.service_agency.getStatus(),"Atendees: [A1]\n Queue: []" )

    def test20_return_three(self):
        service_atendee = self.service_atendee
        attendee1 = service_atendee.helper.create_attendee("A1")
        attendee2 = service_atendee.helper.create_attendee("A2")
        attendee3 = service_atendee.helper.create_attendee("A3")

        attendee_list = self.service.get_all()

        self.assertEquals(3, len(attendee_list))
        self.assertEquals(attendee1, attendee_list[0])
        self.assertEquals(attendee2, attendee_list[1])
        self.assertEquals(attendee3, attendee_list[2])
        self.assertEquals(self.service_agency.getStatus(),"Atendees: [A1,A2,A3]\n Queue: []" )

    def test_initialConfig(self):
        self.service_agency.setName("Burgosland")
        self.service_atendee.assertEqual("Burgosland", self.service_agency.getName())
        self.service_agency.setManager("Joseph")
        self.assertEqual("Joseph", self.service_agency.getManager())

if __name__ == '__main__':
    unittest.main()

    


