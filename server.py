# query: get me the 5 closest stations to 'home'
# from internet >>> Session.query(Cls).order_by(Cls.geom.distance_box('POINT(0 0)')).limit(10)
# 
# home, work = db.Session.query(User.home, User.work).filter_by(User.id==user_id)
# closest_to_home = db.Session.query(Stations).order_by(Stations.geom.distance_box(home)).limit(5)

import os, sys, requests
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, render_template, redirect, request, flash, session
from werkzeug.utils import secure_filename
from model import User, Station, connect_to_db, db
from flask.ext.bcrypt import Bcrypt
from sqlalchemy import exc, desc

app = Flask(__name__)
bcrypt = Bcrypt(app)

#### Setup ###

# Required to use Flask sessions and the debug toolbar
app.secret_key = "B7DB1448B17FB324B053"

# Raise error for undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

#### End Setup ###



if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app, 'postgres:///bike')
    db.create_all()

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug


    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='127.0.0.1')   