"""Data model for go-bike-go.

V1: Two tables: User and Station. 
    Note: Station primary_key is an ID provided directly from citibike
    GeoAlchemy 2 doesn’t currently support other dialects than 
    PostgreSQL/PostGIS. 

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
    home = db.Column(Geography(geometry_type='POINT', srid=4326))
    work = db.Column(Geography(geometry_type='POINT', srid=4326))

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
    point = db.Column(Geography(geometry_type='POINT', srid=4326))

    def __repr__(self):
        return '<Station id:{id}>'.format(id=self.id)

################################################################################

# What the data from the API looks like:
# {"station_id":"79","name":"Franklin St & W Broadway","short_name":"5430.08","lat":40.71911552,"lon":-74.00666661,"region_id":71,"rental_methods":["KEY","CREDITCARD"],"capacity":33,"eightd_has_key_dispenser":false},
# {"station_id":"82","name":"St James Pl & Pearl St","short_name":"5167.06","lat":40.71117416,"lon":-74.00016545,"region_id":71,"rental_methods":["KEY","CREDITCARD"],"capacity":27,"eightd_has_key_dispenser":false},
# {"station_id":"127","name":"Barrow St & Hudson St","short_name":"5805.05","lat":40.73172428,"lon":-74.00674436,"region_id":71,"rental_methods":["KEY","CREDITCARD"],"capacity":31,"eightd_has_key_dispenser":false}

def example_data():
    """Add some example stations and a user to the db"""

    spot1 = "POINT(40.71911552 -74.00666661)"
    spot2 = "POINT(40.71117416 -74.00016545)"
    spot3 = "POINT(40.73172428 -74.00674436)"
    station1 = Station(id=79, name="Franklin St & W Broadway", point=spot1)
    station2 = Station(id=82, name="St James Pl & Pearl St", point=spot2)
    station3 = Station(id=127, name="Barrow St & Hudson St", point=spot3)

    db.session.add_all([station1, station2, station3])
    db.session.commit()

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
        example_data()




