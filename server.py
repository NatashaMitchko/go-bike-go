# query: get me the 5 closest stations to 'home'
# from internet >>> Session.query(Cls).order_by(Cls.geom.distance_box('POINT(0 0)')).limit(10)
#
# home, work = db.session.query(User.home, User.work).filter_by(User.id==user_id)
# 
# main map view, login/register, touch id for login

from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Station
from get_info import seed_station_information, station_status, system_alerts
from geoalchemy2 import func

app = Flask(__name__)
app.secret_key = "ursusmaritimus"
app.jinja_env.undefined = StrictUndefined

#---------------------------------------------------------------------#

@app.route('/')
def index():
    """Show main map view."""

    return render_template('map_view.html')

@app.route('/login')
def test():
	"""Render Login Form"""

	return render_template('login.html')

@app.route('/register')
def register():
	"""Render the registration form"""

	return render_template('register.html')

@app.route('/test')
def test_api():
	"""see if get_info functions work"""
	# seed_station_information() <<< this works now
	point = 'POINT(-73.9713871479 40.7511838746)'
	stations = get_closest_stations(point)
	print stations
	for s in stations:
		print s.name
	return render_template('test.html', stations=stations)

def get_closest_stations(location):
	"""Given a location (home, work, or the user location), return the top 5
	closest stations to that point"""

	query = db.session.query(Station).order_by(func.ST_Distance(Station.point, 
			location)).limit(5)
	return query.all()


#---------------------------------------------------------------------#

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, 'postgres:///bike_test')
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
