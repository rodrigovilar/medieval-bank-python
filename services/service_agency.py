from datetime import datetime
from persistence.models import Attendee, engine
from persistence.models import Demand, engine
from sqlalchemy.orm import sessionmaker
from errors.exceptions import MedievalBankException
from errors.messages import AttendeeMessages
import re

Session = sessionmaker(bind=engine)


# refactor do helper, extract method nas validações do update e create

class AgencyService:
    _session = None
    _attendee_service = None
    _demand_service = None
    _agency_service = None
    name = None
    manager = None
    tick = 0

    def open_session(self):
        self._session = Session()

    def close_session(self):
        self._session.close()

    def __init__(self, attendee_service, demand_service):
        self._attendee_service = attendee_service
        self._demand_service = demand_service


    def resetTick(self):
        self._session.tick = 0


    def increaseTick(self):
        self._session.tick += 1


    def getTick(self):
        return self._session.tick

    def createDemand(self, demand):
        self._demand_service.create(demand)

    def deleteDemandOfTheDemand(self, demand):
        self._demand_service.delete(demand)

    #Não sei como criar um atendee aqui
    def setDemandToAtendee(self, demand, atendeeId):
        return ""

    def getStatusWhithTicks:
        return ""

    def getStatus(self):
        return "Atendees: []\n Queue[]"

    def setName(self, name):
        self._session.nome = name

    def setManager(self, manager):
        self._session.manager = manager
