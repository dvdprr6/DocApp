import json
import datetime

from doctor.db.models import (Doctors, Specialist)
from .common import DoctorRegistrationAPITestCase
from .test_data import (ENDPOINTS, TEST_REGISTER_DOCTOR, REGISTER_DOCTOR_RETURN_ATTRIBUTES,
    TEST_EXPECTED_RETURN_DOCTOR, TEST_EXPECTED_RETURN_SPECIALIST)

# solves the issue where the date can't be json serialized
def serialize_date(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

class TestRegisterDoctors(DoctorRegistrationAPITestCase):

    def test_register_doctor(self):
        request_url = ENDPOINTS['home']
        registration_doctor_info = TEST_REGISTER_DOCTOR
        expected_doctor_result = TEST_EXPECTED_RETURN_DOCTOR
        expected_specialist_result = TEST_EXPECTED_RETURN_SPECIALIST
        response = self.fetch_request(
            request_url,
            method='POST',
            body=json.dumps(registration_doctor_info, default=serialize_date)
        )
        response_list = self.convert_byte_string_to_JSON(response)['data']['doctors_data']
        # print(list(response_list.items()))
        self.get_json_values(response_list)
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