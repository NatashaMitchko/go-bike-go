import unittest

from server import app
from model import connect_to_db

class TestHelperFunctions(unittest.TestCase):
	"""Tests for the helper functions in the server
	login_attempt_successful()
	get_user_by_username()
	get_closest_stations()
	"""

	def setUp(self):
		self.client = app.test_client()
		app.config['TESTING'] = True
		connect_to_db(app, postgresql:///bike_test)

	def tearDown(self):
		db.session.close()

class AddToDatabase(unittest.TestCase):
	pass