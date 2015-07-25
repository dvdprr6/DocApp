import json
import datetime
import logging

from tornado.web import create_signed_value

from tests.core import BaseAppTestCase

from doctor.db.models import Doctors
from doctor.db.models import Specialist

from .test_data import INITIALIZE_DOCTOR_REGISTATION

logging = logging.getLogger(__name__)

class DoctorRegistrationAPITestCase(BaseAppTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @property
    def db(self):
        return self.get_app().db

    def convert_byte_string_to_JSON(self, response):
        return json.loads(response.body.decode('utf-8'))

    def fetch_request(self, *args, **kwargs):
        headers = self._authenticate_reuqest()
        headers['Content-Type'] = 'application/json'
        kwargs['headers'] = headers
        return self.fetch(*args, **kwargs)

    def _authenticate_reuqest(self):
        app = self.get_app()
        secure_cookie = create_signed_value(app.settings['cookie_secret'], 'test', 'user').decode('utf-8')
        headers = {
            'Cookie':'='.join(secure_cookie)
        }
        return headers


class DoctorRegistrationTestCase(DoctorRegistrationAPITestCase):

    def setUp(self):
        super().setUp()
        self.add_doctors_and_specialist_to_tables()

    def tearDown(self):
        self.remove_doctors_and_specialists_from_tables()
        super().tearDown()

    def add_doctors_and_specialist_to_tables(self):
        for doctor_info in INITIALIZE_DOCTOR_REGISTATION:
            doctors_name = doctor_info['doctors_name']
            specialist_name = doctor_info['specialist_name']
            work_hours = doctor_info['work_hours']

            add_specialist = Specialist(specialist_name=specialist_name)
            self.db.add(add_specialist)
            self.db.commit()
            specialist_response_body = {
                'data':{
                    'specialist_data':add_specialist.to_dict()
                }
            }
            # print(specialist_response_body)

            add_doctor = Doctors(
                doctors_name=doctors_name,
                specialist_id=specialist_response_body['data']['specialist_data']['id'],
                work_hours=work_hours
            )
            self.db.add(add_doctor)
            self.db.commit()
            doctor_response_body = {
                'data':{
                    'doctors_data':add_doctor.to_dict()
                }
            }
            # print(doctor_response_body)

        self._doctor_data_info = self.db.query(Doctors).all()
        self._specialist_data_info = self.db.query(Specialist).all()

    def remove_doctors_and_specialists_from_tables(self):
        for doctor in self._doctor_data_info:
            self.db.delete(doctor)
        self.db.commit()
        self._doctor_data_info = []

        for specialist in self._specialist_data_info:
            self.db.delete(specialist)
        self.db.commit()
        self._specialist_data_info = []

class RetrieveAllDoctorRegistrationTestCase(DoctorRegistrationTestCase):
        def setUp(self):
            super().setUp()

        def tearDown(self):
            super().tearDown()