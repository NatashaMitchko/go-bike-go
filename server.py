# home, work = db.session.query(User.home, User.work).filter_by(User.id==user_id)
# 

from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import bcrypt
from geoalchemy2 import func

from model import connect_to_db, db, User, Station
from get_info import seed_station_information, station_status, system_alerts

app = Flask(__name__)
app.secret_key = "ursusmaritimus"
app.jinja_env.undefined = StrictUndefined


#---------------------------------------------------------------------#
# Helper Functions
#---------------------------------------------------------------------#

def get_user_by_username(username):
    """Takes username and returns user object, else returns None """
    user = User.query.filter(User.username==username).first()
    return user
    
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
    app.jinja_env.cache = {}

@app.route('/')
def index():
    """Show main map view. """

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
    	password = request.form.get('password')

    	# Handle getting home and work points

@app.route('/test')
def test_stuff_here():
	"""see if get_info functions work"""
	# seed_station_information() <<< this works now
	point = 'POINT(-73.9713871479 40.7511838746)'
	stations = get_closest_stations(point)
	print stations
	for s in stations:
		print s.name
	return render_template('test.html', stations=stations)


#---------------------------------------------------------------------#
# JSON Routes
#---------------------------------------------------------------------#

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, 'postgres:///bike_test')
    # DebugToolbarExtension(app)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.run(port=5000, host="0.0.0.0")
