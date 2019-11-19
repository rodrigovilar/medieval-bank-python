from datetime import datetime
from persistence.models import Attendee, engine
from sqlalchemy.orm import sessionmaker
from errors.exceptions import MedievalBankException
from errors.messages import AttendeeMessages
import re

Session = sessionmaker(bind=engine)


class AttendeeService:
    _session = None
    _MAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def open_session(self):
        self._session = Session()

    def close_session(self):
        self._session.close()

    def create(self, attendee):
        if not attendee.name:
            raise MedievalBankException(AttendeeMessages.NON_NULLABLE_NAME)

        exists_by_name = self._session.query(Attendee).filter_by(name=attendee.name)
        if len(exists_by_name.all()) > 0:
            raise MedievalBankException(AttendeeMessages.UNIQUE_NAME)

        if attendee.id is not None:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_ID)
        elif attendee.creation_date is not None:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_CREATION_DATE)

        if attendee.email is not None:
            if not re.match(self._MAIL_REGEX, attendee.email):
                raise MedievalBankException(AttendeeMessages.WRONG_FORMAT_EMAIL)

        self._session.add(attendee)
        self._session.commit()

        return attendee

    def get_one(self, attendee_id):
        attendee = self._session.query(Attendee).get(attendee_id)
        if attendee is None:
            raise MedievalBankException(AttendeeMessages(attendee_id).UNKNOWN_ID)
        return attendee

    def update(self, attendee):

        if attendee.name is None:
            raise MedievalBankException(AttendeeMessages.NON_NULLABLE_NAME)

        if attendee.email is not None:
            if not re.match(self._MAIL_REGEX, attendee.email):
                raise MedievalBankException(AttendeeMessages.WRONG_FORMAT_EMAIL)

        db_rep = self.get_one(attendee.id)
        if db_rep.ssn != attendee.ssn:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_SSN)
        elif attendee.creation_date != db_rep.creation_date:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_CREATION_DATE)
        elif attendee.id != db_rep.id:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_ID)

        elif attendee.name != db_rep.name:
            exists_by_name = self._session.query(Attendee).filter_by(name=attendee.name)
            if len(exists_by_name.all()) > 0:
                raise MedievalBankException(AttendeeMessages.UNIQUE_NAME)

        db_rep.name = attendee.name
        db_rep.email = attendee.email

        self._session.commit()
        return db_rep

    def delete(self, attendee):
        attendee = self.get_one(attendee.id)
        self._session.delete(attendee)
        self._session.commit()

    def get_all(self):
        pass

    def find_by_name(self, name):
        pass
