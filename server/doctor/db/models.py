import logging
import datetime
import hashlib

from sqlalchemy import (create_engine, Table, Column, Integer,
	BigInteger, String, DateTime, Text, Boolean, Float, ForeignKey, desc)
from sqlalchemy.orm import relationship, column_property, backref
from sqlalchemy.ext.declarative import declarative_base

log = logging.getLogger(__name__)

Base = declarative_base()
DbMetadata = Base.metadata

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


'''
Doctors[] <-> Patients[]
'''
doctors_patients_association = Table('doctors_patients', DbMetadata,
	Column('doctors_id', Integer, ForeignKey('doctors.id'), primary_key=True),
	Column('patients_id', Integer, ForeignKey('patients.id'), primary_key=True)
)

'''
Specialist[] -> Doctors[]
'''
class Specialist(Base):
	__tablename__ = 'specialist'

	id = Column(Integer, primary_key=True, nullable=False)
	specialist_name = Column(String(255))

	doctor_association = relationship('Doctors')

	def to_dict(self):
		return{
			'id':self.id,
			'specialist_name':self.specialist_name
		}

'''
Doctors[] <- Specialist[]
'''
class Doctors(Base):
	__tablename__ = 'doctors'

	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(255))
	specialist_id = Column(Integer, ForeignKey('specialist.id'), primary_key=True)

	specialist_association = relationship('Specialist', cascade='save-update, merge, delete, delete-orphan')

	patients_association = relationship('Patients', secondary=doctors_patients_association, backref='doctors')

	def to_dict(self):
		return{
			'id':self.id,
			'name':self.name,
			'specialist_id':self.specialist_id
		}



'''
Patients[] <- PatientStatus[]
'''
class Patients(Base):
	__tablename__ = 'patients'

	id = Column(Integer, primary_key=True, nullable=False)
	patient_name = Column(String(255))
	appointment_date = Column(DateTime, default=datetime.datetime.utcnow)
	status_code_id = Column(Integer, ForeignKey('patient_status.id'), primary_key=True)

	pateint_status_association = relationship('PatientStatus', cascade='save-update, merge, delete, delete-orphan')

	def to_dict(self):
		return{
			'id':self.id,
			'patient_name':self.patient_name,
			'appointment_date':self.appointment_date.strftime(DATE_FORMAT),
			'status_code_id':self.status_code_id
		}

'''
PatientStatus[] -> Patients[]
'''
class PatientStatus(Base):
	__tablename__ = 'patient_status'

	id = Column(Integer, primary_key=True, nullable=False)
	status_code = Column(String(13))

	patient_association = relationship('Patients')

	def to_dict(self):
		return{
			'id':self.id,
			'status_code':self.status_code
		}