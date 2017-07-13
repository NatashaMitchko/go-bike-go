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
	seed_station_information()
	return '<h1>Hi</h1>'



#---------------------------------------------------------------------#

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, 'postgres:///bike_test')
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
