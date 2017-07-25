import unittest

from server import app
from model import connect_to_db, db

import server
import get_info

class TestHelperFunctions(unittest.TestCase):
	"""Tests helper functions that do not interface
	with the database"""

class TestHelperFunctionsDB_Read(unittest.TestCase):
	"""Tests helper functions that read from the database
	get_user_by_username()
	get_closest_stations()"""

class TestHelperFunctionsDB_Write(unittest.TestCase):
	"""Tests helper functions that write to the database
	create_new_user()
	seed_station_data()
	"""

	def setUp(self):
		self.client = app.test_client()
		app.config['TESTING'] = True
		connect_to_db(app, postgresql:///bike_test)
		db.create_all()

	def tearDown(self):
		db.session.close()
		db.drop_all()

	def test_create_new_user(self):
		"""Create new user takes the immutable dict request.from
		and creates a new user record."""

		data = {'username': u'Test_User',
					'password': u'test',
					'work': u'88 7th Avenue, New York, NY, United States'
					'home': u'152 Lexington Avenue, New York, NY, United States',
					'homeLngLat', u'-73.98199699999998 40.743772',
					'workLngLat', u'-74.0014936 40.7396046'}

		# Add Test_User to the database
		server.create_new_user(data)

		new_user = db.session.query(User).filter(User.username=='Test_User').one()

		# new_user would return none if it did not exist in the db
		self.assertTrue(new_user)
		self.assertNotEqual(new_user.password, 'password', 'Password likely not hashed before stored in db.')

	def test_seed_station_information(self):
		"""Fetches the station information from the Citibike API
		and adds stations to the database with bike/dock values of 0"""
		get_info.seed_station_information()

		MacDougal_Prince = db.session.query(Station).filter(Station.id == 128).one
		self.assertTrue(MacDougal_Prince)







class TestRoutes(unittest.TestCase):
	"""End to end testing of all routes """

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_login_get(self):
		pass

	def test_login_post(self):
		pass

	def test_register_get(self):
		pass

	def test_register_post(self):
		pass

		# response = self.client.post('/register',
		# 	data = {'username': u'Test_User',
		# 			'password': u'test',
		# 			'work': u'88 7th Avenue, New York, NY, United States'
		# 			'home': u'152 Lexington Avenue, New York, NY, United States',
		# 			'homeLngLat', u'-73.98199699999998 40.743772',
		# 			'workLngLat', u'-73.98199699999998 40.743772'
		# 	}, follow_redirects=True)


if __name__ == "__main__":

    os.system('dropdb bike_test')
    os.system('createdb bike_test')
    os.system('psql bike_test')
    os.system('CREATE EXTENSION postgis;')
    os.system('/q')
    unittest.main()




