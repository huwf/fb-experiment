import sqlalchemy

from sqlalchemy import (create_engine, ForeignKey, Column, String, Text,
    DateTime, Interval, Float, Enum, UniqueConstraint, Boolean, Integer)
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, column_property
from sqlalchemy.orm.exc import NoResultFound, FlushError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import and_
from sqlalchemy import select, func, exists, case, literal_column

Base = declarative_base()


class PopularPasswords(Base):
    __tablename__ = 'PopularPasswords'

    id = Column(Integer, autoincrement=True, primary_key=True)
    rank = Column(Integer)
    # Use sha256
    hash = String(length=64)

    # def __repr__(self):
    #     return 'PopularPasswords(<>)'


class ReceivedPasssword(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    hash = String(length=64)


class PasswordAnalysis(Base):
    __tablename__ = 'PasswordAnalysis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash_id = Column(Integer, ForeignKey(ReceivedPasssword.id))
    # These need to be done before we start hashing the password
    length = Column(Integer)
    all_lowercase = Column(Boolean, default=False)
    same_as_email = Column(Boolean, default=False)



class AnonymisedPersonalInformation(Base):
    __tablename__ = 'PersonalInformation'

    nationality = Column(String(length=40))
    current_country = Column(String(length=40))
    dob = Column(DateTime, nullable=True)
    age = Column(Integer, nullable=True)
    password_id = Column(Integer, ForeignKey(PasswordAnalysis.id))
    provided_password = Column(Boolean, nullable=False, default=True)


class Pings(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    condition = Column(String(length=40))
    user_agent = Column(String(length=256))


class DebriefEmails(Base):
    """
    This table contains the email addresses of people who have taken part, in order to debrief them after
    the conclusion of the study.
    """
    __tablenames__ = 'DebriefEmails'
    id = Column(Integer, autoincrement=True, primary_key=True)
    email_address = Column(String(length=128))
    extra_information = Column(Boolean, default=False)









