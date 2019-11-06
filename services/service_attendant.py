from datetime import datetime
from persistence.models import Attendee, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


class AttendeeService:
    session = None

    def open_session(self):
        self.session = Session()

    def close_session(self):
        self.session.close()

    def create(self, attendee):
        self.session.add(attendee)
        self.session.commit()
        return attendee

    def get_one(self, attendee_id):
        attendee = self.session.query(Attendee).get(attendee_id)
        self.session.expunge(attendee)
        return attendee

    def update(self, attendee):
        pass

    def delete(self, attendee):
        pass

    def get_all(self):
        pass

    def find_by_name(self, name):
        pass
