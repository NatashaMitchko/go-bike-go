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



