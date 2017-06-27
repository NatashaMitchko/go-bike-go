"""Data model for go-bike-go.

V1: Two tables: User and Station. 
    Note: Station primary_key is an ID provided directly from citibike

Class names are singular - table names are plural"""

from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography

db = SQLAlchemy()

class User(db.Model):
    """Basic information about the user including home and work locations."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                    nullable=False, 
                    autoincrement=True, 
                    primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    home = db.Column(Geography(geometry_type='POINT'), srid=4326)
    work = db.Column(Geography(geometry_type='POINT'), srid=4326)

    def __repr__(self):
        return '<User id:{id} username:{username}>'.format(username=self.username,
                                                            id=self.id)

class Station(db.Model):
    """Stores information about all available bike stations. Does not store bike
                availability information"""

    __tablename__ = 'stations'

    id = db.Column(db.Integer, 
                    nullable=False, 
                    autoincrement=False, 
                    primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    point = db.Column(Geography(geometry_type='POINT'), srid=4326)

    def __repr__(self):
        return '<Station id:{id}>'.format(id=self.id)

################################################################################

# What the data from the API looks like:
# {"station_id":"79","name":"Franklin St & W Broadway","short_name":"5430.08","lat":40.71911552,"lon":-74.00666661,"region_id":71,"rental_methods":["KEY","CREDITCARD"],"capacity":33,"eightd_has_key_dispenser":false},
# {"station_id":"82","name":"St James Pl & Pearl St","short_name":"5167.06","lat":40.71117416,"lon":-74.00016545,"region_id":71,"rental_methods":["KEY","CREDITCARD"],"capacity":27,"eightd_has_key_dispenser":false},

def example_data():
    # wkt_spot1 = "POINT(-81.40 38.08)"
    # spot1 = Spot(name="Gas Station", height=240.8, geom=WKTSpatialElement(wkt_spot1))
    # wkt_spot2 = "POINT(-81.42 37.65)"
    # spot2 = Spot(name="Restaurant", height=233.6, geom=WKTSpatialElement(wkt_spot2))

################################################################################    

def init_app():
    """Creating Flask app in order to run SQLAlchemy"""

    from flask import Flask
    app = Flask(__name__)

    # this file connects to a test db
    connect_to_db(app, 'postgres:///bike_test')
    print "Connected to DB."


def connect_to_db(app, database_URI):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = database_URI
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':

        init_app()
        db.create_all()




