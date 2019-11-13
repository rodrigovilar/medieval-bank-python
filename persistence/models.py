from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from persistence import db_path

engine = create_engine('sqlite:///' + db_path, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Attendee(Base):
    """Each class represents a database table"""
    __tablename__ = 'attendee_db'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(255), nullable=False, unique=True)
    creation_date = Column('creation_date', DateTime, default=datetime.utcnow, nullable=False)
    email = Column('email', String(255))
    ssn = Column('ssn', String(255))


def initiate_engine_session_base(engine_path, echo=True):
    _engine = create_engine('sqlite:///' + engine_path, echo=echo)
    _Session = sessionmaker(bind=_engine)
    _Base = declarative_base()
    return _engine, _Session, _Base


def tear_down_test_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

