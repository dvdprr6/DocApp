import logging
import json
import datetime

import tornado
import tornado.gen

from collections import OrderedDict

from tornado.web import HTTPError

from sqlalchemy.exc import SQLAlchemyError

from ..db.models import Doctors
from ..db.models import Specialist

from ..handlers import BaseRequestHandler

logging = logging.getLogger(__name__)

DOCTOR_REG_DATE_FORMAT = '%Y-%m-%d'

class DoctorRegistrationRequestHandler(BaseRequestHandler):
    def exit_with_error(self, status_code, error_message, error_to_log=None):
        if error_to_log:
            log.error(error_to_log)
        self.set_status(status_code)
        self.write({'error':{'message':error_message}})
        self.finish()

    def prepare(self):
        if self.request.body:
            try:
                self.request_body = json.loads(self.request.body.decode('utf-8'))
            except ValueError as ex:
                self.exit_with_error(400, 'Bad Request: Invalid JSON', ex)

    def check_fields_keys(self, field_keys, data):
        code = None
        error_message = None
        for key in field_keys:
            if not key in data:
                error_message = 'Bad Request: Missing attribute: {0}'.format(key)
        return code, error_message

    def exit_with_success(self, status_code, message):
        self.set_status(status_code)
        if message != None:
            self.write(message)
        self.finish()


class DoctorRegistrationHandler(DoctorRegistrationRequestHandler):

    @tornado.web.asynchronous
    def post(self):
        doctors_reg_info_data = self.request_body
        field_keys = [
            'doctors_name',
            'specialist_name',
            'work_hours',
            'registration_date'
        ]
        (response_code, response_body) = self.check_fields_keys(field_keys, doctors_reg_info_data)
        if response_code == 400:
            self.exit_with_error(response_code, response_body)
        else:
            (response_body, response_code) = self._check_dublicate_doctor(doctors_reg_info_data)
            if response_code == 409 or response_code == 500:
                self.exit_with_error(response_code, response_body)
            else:
                self._register_doctor(doctors_reg_info_data)

    def _check_dublicate_doctor(self, doctors_reg_info_data):
        doctors_name = doctors_reg_info_data['doctors_name']
        try:
            duplicate_doctor = self.db.query(Doctors).filter_by(
                doctors_name=doctors_reg_info_data['doctors_name']
            )
            if duplicate_doctor.first() != None:
                response_body = 'Conflict Error: Doctor already exists'
                # print(duplicate_doctor.first().to_dict())
                response_code = 409
            else:
                response_body = None
                response_code = None
        except SQLAlchemyError as ex:
            response_body = 'Internal Server Error: Unable to verify conflict'
            response_code = 500

        return response_body, response_code


    def _register_doctor(self, doctors_reg_info_data):
        specialist_name = doctors_reg_info_data['specialist_name']

        (response_body_specialist, response_code_specialist) = self._add_specialist(specialist_name)

        if response_code_specialist == 500:
            self.exit_with_error(response_code_specialist, response_body_specialist)
        else:
            specialist_response_id = response_body_specialist['data']['specialist_data']['id']
            (response_body_doctor, response_code_doctor) = self._add_doctor(doctors_reg_info_data, specialist_response_id)
            if response_code_doctor == 500:
                self.exit_with_error(response_code_doctor, response_body_doctor)
            else: 
                self.exit_with_success(response_code_doctor, response_body_doctor)

    def _add_specialist(self, specialist_name):
        try:
            add_specialist = Specialist(specialist_name=specialist_name)
            self.db.add(add_specialist)
            self.db.commit()
            response_body = {
                'data':{
                    'specialist_data':add_specialist.to_dict()
                }
            }
            response_code = 201
        except SQLAlchemyError as ex:
            response_body = 'Internal Server Error: Unable to add specialist'
            response_code = 500

        return response_body, response_code

    def _add_doctor(self, doctors_reg_info_data, specialist_response_id):
        try:

            add_doctor = Doctors(
                doctors_name=doctors_reg_info_data['doctors_name'],
                specialist_id=specialist_response_id,
                work_hours=doctors_reg_info_data['work_hours']
            )
            self.db.add(add_doctor)
            self.db.commit()
            response_body = {
                'data':{
                    'doctors_data':add_doctor.to_dict()
                }
            }
            response_code = 201
        except SQLAlchemyError as ex:
            response_body = 'Internal Server Error: Unable to add specialist'
            response_code = 500

        return response_body, response_code

class RetrieveAllDoctorRegistrationHandler(DoctorRegistrationRequestHandler):

    @tornado.web.asynchronous
    def get(self):
        try:
            all_doctors = self.db.query(
                Doctors.doctors_name,
                Specialist.specialist_name,
                Doctors.work_hours,
                Doctors.registration_date
            ).join(Specialist).filter(
                Doctors.specialist_id==Specialist.id
            ).all()
            response_code = 200
        except SQLAlchemyError as ex:
            response_body = 'Internal Server Error: Unable to retrieve Doctors'
            response_code = 500

        if response_code == 500:
            self.exit_with_error(response_code, response_body)
        else:
            response_body = self._create_response_body_all_doctors(all_doctors)
            # print(response_body)
            self.exit_with_success(response_code, response_body)

    def _create_response_body_all_doctors(self, all_doctors):
        response_body = {'data':{'doctors': []}}
        for doctor in all_doctors:
            result = {
                'doctors_name':doctor.doctors_name,
                'specialist_name':doctor.specialist_name,
                'work_hours':doctor.work_hours,
                'registration_date':doctor.registration_date.strftime(DOCTOR_REG_DATE_FORMAT)
            }
            response_body['data']['doctors'].append(result)

        return response_body



