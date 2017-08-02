# home, work = db.session.query(User.home, User.work).filter_by(User.id==user_id)
# 

from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import bcrypt
import re
from geoalchemy2 import func
from sqlalchemy import exc

from model import connect_to_db, db, User, Station
from get_info import seed_station_information, update_station_status, system_alerts

app = Flask(__name__)
app.secret_key = "ursusmaritimus"
app.jinja_env.undefined = StrictUndefined


#---------------------------------------------------------------------#
# Helper Functions
#---------------------------------------------------------------------#

def create_new_user(user_info):
	"""This function takes the request.form objcet passed to the register route and
	parses it out to create a new user in the database."""

	home = 'POINT(' + user_info['homeLngLat'] + ')'
	work = 'POINT(' + user_info['workLngLat'] + ')'

	new_user = User(username = user_info['username'],
					password = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt()),
					home_address = user_info['home'],
					work_address = user_info['work'],
					home_point = home,
					work_point = work)
	try:
		db.session.add(new_user)
		db.session.commit()
	except exc.IntegrityError:
		db.session.rollback()

def get_user_by_id(id):
	"""Takes user id and returns user object"""
	return User.query.filter(User.id==id).first()

def get_user_by_username(username):
    """Takes username and returns user object, else returns None """
    return User.query.filter(User.username==username).first()
    
def login_attempt_sucessful(username, password):
	"""Checks to see if the username/password combination is valid. 
	If the combination is valid the user object is returned. The user must exist
	and have entered the correct password else the function returns false.
	"""
	user = get_user_by_username(username)
	if user and bcrypt.hashpw(password, hashed) == hashed:
		return user
	else:
		return False 

def get_closest_stations(location):
	"""Given a location (home, work, or the user location), return the top 5
	closest stations to that point"""

	query = db.session.query(Station).order_by(func.ST_Distance(Station.point, 
		location)).limit(5)

	return query.all()

#---------------------------------------------------------------------#
# Routes
#---------------------------------------------------------------------#

@app.before_request
def before_request():
    # When you import jinja2 macros, they get cached which is annoying for local
    # development, so wipe the cache every request.
    session['active'] = True
    session['user_id'] = 1
    app.jinja_env.cache = {}

@app.route('/')
def index():
    """Show main map view. """
    if session['active']:
    	user = get_user_by_id(session['user_id'])
    	home = get_closest_stations(user.home_point)
    	work = get_closest_stations(user.work_point)

    	return render_template('test.html', user=user, home=home, work=work)

    return render_template('map_view.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Render Login Form and handle login form submissions. """
	if request.method == 'GET':
		return render_template('login.html')
	else:
		username = request.form.get('username')
    	password = request.form.get('password')

    	logged_in_user = login_attempt_sucessful(username, password)

    	if logged_in_user:
    		session['active'] = True
    		session['user_id'] = user.id
    		return redirect('/')
    	else:
    		flash('Incorrect username or password')
    		return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Render the registration form and handle regestration events. """
	if request.method == 'GET':
		return render_template('register.html')
	else:
		username = request.form.get('username')
		print request.form
    	if get_user_by_username(username):
    		flash('Username Taken')
    		return redirect('/register')
    	else:
    		create_new_user(request.form)
    		print "new user created"
    		return redirect('/')

@app.route('/seed')
def seed_and_update():
	"""seed and update the database - temporart solution"""
	seed_station_information()
	print 'Seeded'
	update_station_status()
	print 'Stations updated'

	return '<h1>DB Seeded</h1>'


#---------------------------------------------------------------------#
# JSON Routes
#---------------------------------------------------------------------#

@app.route('/home.json')
def send_home_availability():
	"""Sends JSON about home bike stations and availability"""
	user = get_user_by_id(session['user_id'])
	home = get_closest_stations(user.home_point)

	stations = {}

	for i in range(len(home)):
		coords = re.match(r'\(-?([^\)]+)\)', '(-74.00016545 40.71117416)').group()
		lon, lat = coords[1:-1].split()
		stations[str(i)] = {'name': home[i][0].name,
										'bikes': home[i][0].num_bikes_available,
										'docks': home[i][0].num_docks_available,
										'lat': lat,
										'lon': lon
										}
	return jsonify(stations)



@app.route('/work.json')
def send_work_availability():
	"""Sends JSON about work bike stations and availability"""
	user = get_user_by_id(session['user_id'])
	work = get_closest_stations(user.work_point)

	stations = {}

	for i in range(len(work)):
		coords = re.match(r'\(-?([^\)]+)\)', '(-74.00016545 40.71117416)').group()
		lon, lat = coords[1:-1].split()
		stations[str(i)] = {'name': work[i][0].name,
										'bikes': work[i][0].num_bikes_available,
										'docks': work[i][0].num_docks_available,
										'lat': lat,
										'lon': lon
										}
	return jsonify(stations)

@app.route('/user-location.JSON')
def send_user_location_availability(location):
	"""Gets location from the user and finds closest stations and availability"""



if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, 'postgres:///bike')
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run(port=5000, host="0.0.0.0")
