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

		https://gbfs.citibikenyc.com/gbfs/en/station_information.json"""

	response = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json')
	response = json.loads(response.text)

	for station in response['data']['stations']:
		point = 'POINT(' + str(station['lon']) + ' ' + str(station['lat']) + ')'

		print point
		new_station = Station(
							id = int(station['station_id']),
							name = station['name'],
							point = point
								)
		try:
			db.session.add(new_station)
			db.session.commit()
		except exc.IntegrityError:
			db.session.rollback()


def station_status(station_id):
	"""Parses out status for a particular station.
			
		https://gbfs.citibikenyc.com/gbfs/en/station_status.json"""

	pass

def system_alerts():
	"""Get alerts about the system. 

		https://gbfs.citibikenyc.com/gbfs/en/system_alerts.json"""
	pass

