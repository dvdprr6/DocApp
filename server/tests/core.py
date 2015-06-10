import unittest
import configparser

from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine_from_config

from doctor.webserver import WebApplication

config = configparser.RawConfigParser()
config.read('conf/test/docs.conf')

app = WebApplication(config=config)

class BaseAppTestCase(AsyncHTTPTestCase, LogTrapTestCase):

	def setUp(self):
		super().setUp()
		self._start()

	def tearDown(self):
		self._end()
		super().tearDown()

	def _start(self):
		pass

	def _end(self):
		pass

	def get_app(self):
		return app