import sqlalchemy
import requests
import hashlib
import re

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
    hash = Column(String(length=64))

    # def __repr__(self):
    #     return 'PopularPasswords(<>)'




class ReceivedPasssword(Base):
    __tablename__ = 'Passwords'

    id = Column(Integer, autoincrement=True, primary_key=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    hash = String(length=64)
    salt = String(length=32)




class PasswordAnalysis(Base):
    __tablename__ = 'PasswordAnalysis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash_id = Column(Integer, ForeignKey(ReceivedPasssword.id))
    # These need to be done before we start hashing the password
    length = Column(Integer)
    all_lowercase = Column(Boolean, default=False)
    all_letters = Column(Boolean, default=False)
    all_numbers = Column(Boolean, default=False)
    same_as_email = Column(Boolean, default=False)
    # Uses the RockYou list
    popular_password = Column(Boolean, default=False)
    # If it's -1 then it's not on the list
    password_rank = Column(Integer, default=-1)
    # Indicates password reuse
    have_i_been_pwned = Column(Boolean, default=False)

    def is_all_lowercase(self, password):
        return password.lower() == password

    def is_all_letters(self, password):
        return bool(re.fullmatch('[A-Za-z]+', password))

    def is_all_numbers(self, password):
        return bool(re.fullmatch('\d+', password))

    def is_same_as_email(self, email, password):
        return email == password

    def is_pwned(self, password):
        sha1_pw = hashlib.sha1(bytes(password, encoding='utf-8')).hexdigest()
        resp = requests.post('https://haveibeenpwned.com/api/v2',
                             headers={'Content-type': 'application/x-www-form-urlencoded'},
                             data={'Password': sha1_pw})
        # If status is OK then the password exists
        # If it's 404 then it does not
        return resp.status_code == 200

    def password_length(self, password):
        return len(password)

class AnonymisedPersonalInformation(Base):
    import random
    __tablename__ = 'PersonalInformation'
    id = Column(Integer, primary_key=True)
    nationality = Column(String(length=40))
    current_country = Column(String(length=40))
    dob = Column(DateTime, nullable=True)
    age = Column(Integer, nullable=True)
    password_id = Column(Integer, ForeignKey(PasswordAnalysis.id))
    provided_password = Column(Boolean, nullable=False, default=True)


class Pings(Base):
    __tablename__ = 'Pings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    condition = Column(String(length=40))
    user_agent = Column(String(length=256))


class DebriefEmails(Base):
    """
    This table contains the crowdflower IDs of people who took part, 
    so we can contact them after the study with the Crowdflower API.
    """
    __tablename__ = 'DebriefEmails'
    id = Column(Integer, autoincrement=False, primary_key=True)


def populate_rockyou(db_url):
    engine = create_engine(db_url)
    db = scoped_session(sessionmaker(autoflush=True, bind=engine))
    Base.metadata.create_all(bind=engine)
    import os
    with open(os.path.join(os.getcwd(), 'rockyou.txt'), encoding='latin-1') as f:
        i = 1
        for pw in f.readlines():
            sha_pw = hashlib.sha256(bytes(pw, encoding='latin-1')).hexdigest()
            password_obj = PopularPasswords(rank=i, hash=sha_pw)
            print(pw.split(' ')[len(pw.split(' ')) - 1].strip())
            i += 1
            db.add(password_obj)
            if i > 100000:
                break
        db.commit()


