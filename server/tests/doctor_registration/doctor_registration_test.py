import json
import datetime

from doctor.db.models import (Doctors, Specialist)
from .common import DoctorRegistrationTestCase
from .common import DoctorRegistrationAPITestCase

from .test_data import (
    ENDPOINTS,
    TEST_REGISTER_DOCTOR_FRANK,
    TEST_EXPECTED_RETURN_DOCTOR,
    TEST_EXPECTED_RETURN_SPECIALIST,
    TEST_DUBLICATE_REGISTER_DOCTOR_MARIO
)

# solves the issue where the date can't be json serialized
def serialize_date(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

class TestRegisterDoctors(DoctorRegistrationTestCase):

    '''Standard cases on /doctor_registration/create/'''

    def test_post_register_doctor(self):
        request_url = ENDPOINTS['add_doctor']
        registration_doctor_info = TEST_REGISTER_DOCTOR_FRANK
        expected_doctor_result = TEST_EXPECTED_RETURN_DOCTOR
        expected_specialist_result = TEST_EXPECTED_RETURN_SPECIALIST
        response = self.fetch_request(
            request_url,
            method='POST',
            body=json.dumps(registration_doctor_info, default=serialize_date)
        )
        response_list = self.convert_byte_string_to_JSON(response)['data']['doctors_data']
        # print(list(response_list.items()))
        self.assertEqual(response.code, 201)
        query_doctor = self.db.query(Doctors).filter_by(
            doctors_name=registration_doctor_info['doctors_name']
        )
        specialist_info = query_doctor.first().to_dict()
        query_specialist = self.db.query(Specialist).filter_by(
            id=specialist_info['specialist_id']
        )
        doctor_query_info = query_doctor.first().to_dict()
        specialist_query_info = query_specialist.first().to_dict()
        # print(doctor_query_info)
        # print(specialist_query_info)
        self.db.delete(query_doctor.first())
        self.db.delete(query_specialist.first())
        self.db.commit()

    def test_post_dublicate_register_doctor(self):
        request_url = ENDPOINTS['add_doctor']
        registration_doctor_info = TEST_DUBLICATE_REGISTER_DOCTOR_MARIO
        response = self.fetch_request(
            request_url,
            method='POST',
            body=json.dumps(registration_doctor_info)
        )

        self.assertEqual(response.code, 409)