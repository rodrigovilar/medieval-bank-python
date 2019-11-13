from datetime import datetime
from persistence.models import Attendee, engine
from sqlalchemy.orm import sessionmaker
from errors.exceptions import MedievalBankException
from errors.messages import AttendeeMessages
import re

Session = sessionmaker(bind=engine)


class AttendeeService:
    session = None
    mail_regex = '/^[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.([a-z]+)?$/i'

    def open_session(self):
        self.session = Session()

    def close_session(self):
        self.session.close()

    def create(self, attendee):
        if not attendee.name:
            raise MedievalBankException(AttendeeMessages.NON_NULLABLE_NAME)

        exists_by_name = self.session.query(Attendee).filter_by(name=attendee.name)
        if len(exists_by_name.all()) > 0:
            raise MedievalBankException(AttendeeMessages.UNIQUE_NAME)

        if attendee.id is not None:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_ID)
        elif attendee.creation_date is not None:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_CREATION_DATE)

        self.session.add(attendee)
        self.session.commit()

        return attendee

    def get_one(self, attendee_id):
        attendee = self.session.query(Attendee).get(attendee_id)
        self.session.expunge(attendee)
        return attendee

    def update(self, attendee):
        attendeeAtual = self.get_one(attendee.id)

        if attendeeAtual is None:
            raise MedievalBankException("O obejeto não cadastrado!")
        attendeeAtual.name = attendee.name
        attendeeAtual.email = attendee.email
        return attendeeAtual

    def delete(self, attendee):
        pass

    def get_all(self):
        pass

    def find_by_name(self, name):
        pass
