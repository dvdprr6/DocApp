import json
import datetime

from doctor.db.models import (Doctors, Specialist)
from .common import DoctorRegistrationAPITestCase
from .test_data import ENDPOINTS

# solves the issue where the date can't be json serialized
def serialize_date(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

class TestHome(DoctorRegistrationAPITestCase):
    
    def test_home(self):
        request_url = ENDPOINTS['home']
        expected_response = 'Hello, world'
        response = self.fetch(request_url, method='GET')
        self.assertEqual(response.code, 200)