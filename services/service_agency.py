from datetime import datetime
from persistence.models import Attendee, engine
from sqlalchemy.orm import sessionmaker
from errors.exceptions import MedievalBankException
from errors.messages import AttendeeMessages

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

    def setName(self,name):
        self.name = name


    def setManager(self, manager):
        self.manager = manager

    def status(self):
        return("Atendees: [",self._attendee_service_all(),"]\n Queue: []")

