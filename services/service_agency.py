from datetime import datetime
from persistence.models import Attendee, engine
from sqlalchemy.orm import sessionmaker
from errors.exceptions import MedievalBankException
from errors.messages import AttendeeMessages
import re

Session = sessionmaker(bind=engine)


# refactor do helper, extract method nas validações do update e create


class AgencyService:
    _session = None
    _attendee_service = None
    name = None
    manager = None

    def open_session(self):
        self._session = Session()

    def close_session(self):
        self._session.close()

    def __init__(self, attendee_service):
        self._attendee_service = attendee_service

    @staticmethod
    def setName(self,name):
        self.name = name


    @staticmethod
    def setManager(self, manager):
        self.manager = manager
