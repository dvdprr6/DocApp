import logging
import json

import tornado.web

logging = logging.getLogger(__name__)

class BaseRequestHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def request_body_json(self):
        return json.loads(self.request.body.decode('utf-8'))

'''
Doctor Registration API
'''

# from .doctor_registration.handlers import MainHandler
from .doctor_registration.handlers import DoctorRegistrationHandler

doctor_registration_api = [
    (r'/doctor_registration/?', DoctorRegistrationHandler)
]