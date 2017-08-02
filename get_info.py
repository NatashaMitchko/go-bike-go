""" These are the only functions in the app that interface with the Citibike API

JSON Information about the stations is obtained from these links
"feeds":[  
    {  
       "name":"station_information",
       "url":"https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
    },
    {  
       "name":"system_information",
       "url":"https://gbfs.citibikenyc.com/gbfs/en/system_information.json"
    },
    {  
       "name":"station_status",
       "url":"https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
    },
    {  
       "name":"system_alerts",
       "url":"https://gbfs.citibikenyc.com/gbfs/en/system_alerts.json"
    },
    {  
       "name":"system_regions",
       "url":"https://gbfs.citibikenyc.com/gbfs/en/system_regions.json"
    }
 ]

      """

import requests, json
from model import db, Station
from sqlalchemy import exc

def seed_station_information():
	"""Get's and formats all station information in order to update stations in
	the database.

		point formatting is: 'POINT(lon lat)'

		Bike and dock information is initialized at zero

		https://gbfs.citibikenyc.com/gbfs/en/station_information.json"""

	response = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json')
	response = json.loads(response.text)

	for station in response['data']['stations']:
		point = 'POINT(' + str(station['lon']) + ' ' + str(station['lat']) + ')'

		new_station = Station(
							id = int(station['station_id']),
							name = station['name'],
							point = point,
							num_bikes_available=0, 
							num_docks_available=0)
		try:
			db.session.add(new_station)
			db.session.commit()
		except exc.IntegrityError:
			db.session.rollback()


def update_station_status():
	"""Updates the database with the status of all of the stations.
			
	https://gbfs.citibikenyc.com/gbfs/en/station_status.json"""

	response = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json')
	response = json.loads(response.text)

	for station in response['data']['stations']:
		try:
			s = db.session.query(Station).filter(Station.id == station['station_id'])

			s.update({Station.num_bikes_available: station['num_bikes_available'],
									Station.num_docks_available: station['num_docks_available']})
			db.session.commit()
		except exc.IntegrityError:
			db.session.rollback()

def system_alerts():
	"""Get alerts about the system. 

		https://gbfs.citibikenyc.com/gbfs/en/system_alerts.json"""
	pass


