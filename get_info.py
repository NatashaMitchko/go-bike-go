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


Saving here for now so I don't forget g
118/1: home = POINT(40.720807 -73.987864)
118/2: home = "POINT(40.720807 -73.987864)"
118/3: query = db.Session.query(Station).order_by(Station.geom.distance_box(home)).limit(2)
118/4: Station.order_by(Station.geom.distance_box(home)).limit(5)
118/5: User.query.all()
118/6: Station.query.all()
119/1: db.session.query(Station).order_by(Station.geom.distance_box(home)).limit(5)
119/2: db.session.query(Station).order_by(Station.point.distance_box(home)).limit(5)
119/3: home = "POINT(40.720807 -73.987864)"
119/4: db.session.query(Station).order_by(Station.point.distance_box(home)).limit(5)
119/5: a = db.session.query(Station).order_by(Station.point.distance_box(home)).limit(5)
119/6: a.all()
120/1: home = "POINT(40.720807 -73.987864)"
120/2: a = db.session.query(Station).limit(2).order_by(func.ST_Distance(Station.point, home))
120/3: a = db.session.query(Station).order_by(func.ST_Distance(Station.point, home)).limit(2)
120/4: a
120/5: a.all()
120/6: a = db.session.query(Station).order_by(func.ST_Distance(Station.point, home)).limit(3)
120/7: a.all()

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

		print point
		new_station = Station(
							id = int(station['station_id']),
							name = station['name'],
							point = point,
							num_bikes_available=0, 
							num_docks_available=0
								)
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

