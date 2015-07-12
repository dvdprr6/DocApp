import json
import datetime
import logging

from tornado.web import create_signed_value

from tests.core import BaseAppTestCase
from doctor.db.models import (Doctors, Specialist)

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