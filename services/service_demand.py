from errors.messages import DemandMessages
from errors.exceptions import MedievalBankException
from persistence.models import Demand, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


class DemandService:
    _session = None

    def open_session(self):
        self._session = Session()

    def close_session(self):
        self._session.close()

    def create(self, demand):
        if not demand.name:
            raise MedievalBankException(DemandMessages.NON_NULLABLE_NAME)

        exists_by_name = self._session.query(Demand).filter_by(name=demand.name)
        if len(exists_by_name.all()) > 0:
            raise MedievalBankException(DemandMessages.UNIQUE_NAME)

        if demand.id is not None:
            raise MedievalBankException(DemandMessages.IMMUTABLE_ID)
        if demand.creation_date is not None:
            raise MedievalBankException(DemandMessages.IMMUTABLE_CREATION_DATE)

        self._session.add(demand)
        self._session.commit()

        return demand

    def get_one(self, attendee_id):
        demand = self._session.query(Demand).get(attendee_id)
        if demand is None:
            raise MedievalBankException(DemandMessages(attendee_id).UNKNOWN_ID)
        return demand

    def update(self, demand):
        if demand.name is None:
            raise MedievalBankException(DemandMessages.NON_NULLABLE_NAME)
        old_demand = self.get_one(demand.id)

        if demand.creation_date != old_demand.creation_date:
            raise MedievalBankException(DemandMessages.IMMUTABLE_CREATION_DATE)

        if demand.id != old_demand.id:
            raise MedievalBankException(DemandMessages.IMMUTABLE_ID)

        if demand.name != old_demand.name:
            exists_by_name = self._session.query(Demand).filter_by(name=demand.name)
            if len(exists_by_name.all()) > 0:
                raise MedievalBankException(DemandMessages.UNIQUE_NAME)

        old_demand.name = demand.name

        self._session.commit()
        return old_demand

    def delete(self, demand):
        self._session.delete(demand)
        self._session.commit()

    def get_all(self):
        demand_list = self._session.query(Demand).all()
        return demand_list

    # Não sei como pegar os não alocados
    def get_allUnallocated(self):
        demand_list = self._session.query(Demand).all()
        return demand_list

    def find_by_name(self, name):
        demand_list = self._session.query(Demand).filter(Demand.name.like(f"%{name}%")).all()
        return demand_list
