# Go Bike Go

Inspired by the app [WABA](https://itunes.apple.com/us/app/where-a-bike-at-citibike-nyc/id689093812?mt=8) (where a bike at?), Go Bike Go allows users to quikly find Citibikes on their commute. Users create a profile with their home and work addresses and can easily see bike and dock availability at the endpoints of their commute.

## Database and ORM
### Setting up the database

The database that is connected to the server is a postgreSQL database with the geospatial extension postGIS. This allows the server to ask questions like "what are the 5 closest bike docks available to me that have bikes available?". Enabling postGIS for this project was as simple as making sure the extension is installed, creating a postgreSQL database and enabling the extension in that database.

```
$ createdb go_bike_go
$ psql go_bike_go
go_bike_go=# CREATE EXTENSION postgis;
```

### SQLAlchemy & Geoalchemy2 - The ORM

Once PostGIS was enabled I created the ORM using SQLAlchemy ([model.py](/model.py)). There are two tables in the database that have no relation: User and Station. Both the User and Station store geographic information. 

#### Setting up the ORM

Here is a simplified version of the implementation. The following creates a single table with two columns, a primary key and a point geometry.

```python
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography

db = SQLAlchemy()

class Example(db.Model):
	"""Primary key and point geometry"""

	__tablename__ = 'example'

	id = db.Column(db.Integer,
                   nullable=False,
                   autoincrement=True,
                   primary_key=True)
    point = db.Column(Geography(geometry_type='POINT', srid=4326))
```
#### Adding points to the database
In order to add records to the table the points need to be inputed in [WKT (well-known text)](https://en.wikipedia.org/wiki/Well-known_text) format. For the point geometry the format is 'POINT(lon lat)'. To add the point (40.7047029,-73.9588267) we would do the following:

```python
from sqlalchemy import exc

point = 'POINT(' + '-73.9588267' + ' ' + '40.7047029' + ')'

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
```

#### Getting information out of the database

When attempting to get coordinate points out of the database you get them back in the WKB (well-known binary) format. In order to get them back in WKT, in order to be sent to the Google Maps API for display, they need to be converted back. The GeoAlchemy2 function that does this is ST_AsText. From what I can tell this function can only be executed during the transaction i.e. you cannot get the bike station object and then ask to convert from WKB to WKT on the point attribute. Because of this the conversion needs to happen in the query itself. The helper function ```get_closest_stations(location)``` in the [server](/server.py)takes a location and returns a tuple of the station object and the WKT version of the coordinates.

```python
from geoalchemy2 import func

def get_closest_stations(location):
	"""Given a location (home, work, or the user location), return the top 5
	closest stations to that point"""

	query = db.session.query(Station, 
		func.ST_AsText(Station.point)).order_by(func.ST_Distance(Station.point, 
		location)).limit(5)

	return query.all()
```
