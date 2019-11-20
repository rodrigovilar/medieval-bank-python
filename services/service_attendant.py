from datetime import datetime
from persistence.models import Attendee, engine
from sqlalchemy.orm import sessionmaker
from errors.exceptions import MedievalBankException
from errors.messages import AttendeeMessages
import re

Session = sessionmaker(bind=engine)

# refactor do helper, extract method nas validações do update e create


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

        # Investigar se dá pra fazer de forma melhor
        exists_by_name = self._session.query(Attendee).filter_by(name=attendee.name)
        if len(exists_by_name.all()) > 0:
            raise MedievalBankException(AttendeeMessages.UNIQUE_NAME)

        if attendee.id is not None:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_ID)
        if attendee.creation_date is not None:
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

        old_attendee = self.get_one(attendee.id)
        if old_attendee.ssn != attendee.ssn:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_SSN)
        if attendee.creation_date != old_attendee.creation_date:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_CREATION_DATE)
        if attendee.id != old_attendee.id:
            raise MedievalBankException(AttendeeMessages.IMMUTABLE_ID)

        if attendee.name != old_attendee.name:
            exists_by_name = self._session.query(Attendee).filter_by(name=attendee.name)
            if len(exists_by_name.all()) > 0:
                raise MedievalBankException(AttendeeMessages.UNIQUE_NAME)

        old_attendee.name = attendee.name
        old_attendee.email = attendee.email

        self._session.commit()
        return old_attendee

    def delete(self, attendee):
        if attendee is None:
            raise MedievalBankException(AttendeeMessages.NULL_INSTANCE)

        attendee = self.get_one(attendee.id)
        self._session.delete(attendee)
        self._session.commit()

    def get_all(self):
        attendee_list = self._session.query(Attendee).all()
        return attendee_list

    def find_by_name(self, name):
        attendee_list = self._session.query(Attendee).filter(Attendee.name.like(f"%{name}%")).all()
        return attendee_list
