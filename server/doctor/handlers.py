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

from .doctor_registration.handlers import DoctorRegistrationHandler
from .doctor_registration.handlers import RetrieveAllDoctorRegistrationHandler

doctor_registration_api = [
    # (r'/doctor_registration/home/?', DoctorRegistrationHandler),
    # (r'/doctor_registration/home/create/?', DoctorRegistrationHandler)
    #(?P<id>[a-zA-Z0-9_]+)/?$
    (r'/doctor_registration/?', RetrieveAllDoctorRegistrationHandler),
    (r'/doctor_registration/create/?', DoctorRegistrationHandler)
]