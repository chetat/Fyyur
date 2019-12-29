import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler

db = SQLAlchemy()
moment = Moment()



def create_app(config):
    app = Flask(__name__)
    # App init was here
    app.config.from_object(config)

    initialize_extensions(app)
    migrate = Migrate(app, db)
    return app

def initialize_extensions(app):
    moment.init_app(app)
    db.init_app(app)





