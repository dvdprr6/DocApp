import logging
import datetime
import hashlib

from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import desc
from sqlalchemy.orm import relationship, column_property, backref
from sqlalchemy.ext.declarative import declarative_base

log = logging.getLogger(__name__)

Base = declarative_base()
DbMetadata = Base.metadata

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
DOCTOR_REG_DATE_FORMAT = '%Y-%m-%d'

doctors_patients_association = Table('doctors_patients', DbMetadata,
    Column('doctors_id', Integer, ForeignKey('doctors.id')),
    Column('patients_id', Integer, ForeignKey('patients.id'))
)

class Specialist(Base):
    __tablename__ = 'specialist'

    id = Column(Integer, primary_key=True)
    specialist_name = Column(String(255))
    doctors_association = relationship('Doctors')

    def to_dict(self):
        return{
            'id':self.id,
            'specialist_name':self.specialist_name
        }

class Doctors(Base):
    __tablename__ = 'doctors';

    id = Column(Integer, primary_key=True)
    doctors_name = Column(String(255))
    specialist_id = Column(Integer, ForeignKey('specialist.id'))
    work_hours = Column(Integer, primary_key=False) # per week
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)

    doctors_patients_association = relationship('Patients', secondary=doctors_patients_association)

    def to_dict(self):
        return{
            'id':self.id,
            'doctors_name':self.doctors_name,
            'specialist_id':self.specialist_id,
            'work_hours':self.work_hours,
            'registration_date':self.registration_date.strftime(DOCTOR_REG_DATE_FORMAT)
        }

class PatientStatus(Base):
    __tablename__ = 'patient_status'

    id = Column(Integer, primary_key=True)
    status_code = Column(String(13))
    patient_association = relationship('Patients')

    def to_dict(self):
        return{
            'id':self.id,
            'status_code':self.status_code
        }

class Patients(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    patient_name = Column(String(255))
    appointment_date = Column(DateTime, default=datetime.datetime.utcnow)
    status_id = Column(Integer, ForeignKey('patient_status.id'))

    def to_dict(self):
        return{
            'id':self.id,
            'patient_name':self.patient_name,
            'appointment_date':self.appointment_date.strftime(DATE_FORMAT),
            'status_id':self.status_id
        }