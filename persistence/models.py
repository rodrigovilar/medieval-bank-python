from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///burgos.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Attendee(Base):
    """Each class represents a database table"""
    __tablename__ = 'attendee_db'

    id = Column(Integer, primary_key=True)
    name = Column('name', String(255))
    creation_date = Column('creation_date', DateTime, default=datetime.utcnow)
    email = Column('email', String(255))
    ssn = Column('ssn', String(255))


if __name__ == '__main__':
    Base.metadata.create_all(engine)

