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

    @staticmethod
    def resetTick(self):
        agency_service.tick = 0

    @staticmethod
    def increaseTick(self):
        agency_service.tick += 1

    @staticmethod
    def getTick(self):
        return agency_service.tick

    def createDemand(self, demand):
        self._demand_service.create(demand)

    def deleteDemandOfTheDemand(self, demand):
        self._demand_service.delete(demand)

    #Não sei como criar um atendee aqui
    def setDemandToAtendee(self, demand, atendeeId):
        #Demand demand
        #Atendee atendee
        #atendee = _attendee_service.get_one(atendeeId)
        #atendee.setDemand(demand)

        #demand.setAllocated(true)
        #demand.setAtendee(atendee)
        #_demand_service.update(demand)

        #_attendee_service.update(atendee)

    def getStatusWhithTicks:
        #List < Atendee > listOfTheAteendes = atendeeService.getAll();
        #List < Demand > listOfTheDemands = demandService.getAll();

        #return "Atendees: " + listOfTheAteendes + "\n" + "Queue: " + listOfTheDemands + "\n" + "Tick must return: "+ this.getTick();


    def getStatus:
        #List < Atendee > listOfTheAteendes = atendeeService.getAll();
        #List < Demand > listOfTheDemands = demandService.getAllUnallocated();

        #return "Atendees: " + listOfTheAteendes + "\n" + "Queue: " + listOfTheDemands;


    @staticmethod
    def setName(name):
        agency_service.name = name

    @staticmethod
    def setManager(manager):
        agency_service.manager = manager
