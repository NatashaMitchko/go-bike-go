# Go Bike Go

Inspired by the app [WABA](https://itunes.apple.com/us/app/where-a-bike-at-citibike-nyc/id689093812?mt=8) (where a bike at?), Go Bike Go allows users to quickly find Citibikes on their commute. Users create a profile with their home and work addresses and can easily see bike and dock availability at the endpoints of their commute.

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

new_example = Example(point = point)

try:
	db.session.add(new_example)
	db.session.commit()
except exc.IntegrityError:
	db.session.rollback()
```

#### Getting information out of the database

When attempting to get coordinate points out of the database you get them back in the WKB (well-known binary) format. In order to get them back in WKT, in order to be sent to the Google Maps API for display, they need to be converted back. The GeoAlchemy2 function that does this is ST_AsText. From what I can tell this function can only be executed during the transaction i.e. you cannot get the bike station object and then ask to convert from WKB to WKT on the point attribute. Because of this I've written two methods for the Station class that use the [shapely](https://github.com/Toblerity/Shapely) module to convert the WKB into the latitude and longitude coordinates.

```python
from shapely.wkb import loads

def lat(self):
    """Return the latitude of the station"""
    coordinates = loads(bytes(self.point.data))
    return coordinates.y

def lng(self):
    """Return the longitude of the station"""
    coordinates = loads(bytes(self.point.data))
    return coordinates.x
```
## Updating the Station Bike and Dock Counts

The bike and dock counts are updated by the process running out of [update.py](/update.py). This script creates a Flask-app instance in order to use Flask-SQLAlchemy, connects to the database and then runs ```update_station_status()``` every 60 seconds. The scheduling is controlled by a simple timer in a while loop. The update itself takes approximately 1.5 seconds to complete.