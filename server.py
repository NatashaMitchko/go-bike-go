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

app = Flask(__name__)
app.secret_key = "ursusmaritimus"
app.jinja_env.undefined = StrictUndefined

#---------------------------------------------------------------------#

@app.route('/')
def index():
    """Show homepage."""

    return render_template("test.html")

@app.route('/hi')
def test():
	"""Test showing a map"""

	return render_template('map_view.html')


#---------------------------------------------------------------------#

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, 'postgres:///bike_test')
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
