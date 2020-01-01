import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
# DONE IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://xwctarovbqsuxz:cf11b2bf0a52cba8410b9bd633706a40c4f2d529422ec53b2a06b9a1eb87f013@ec2-174-129-255-57.compute-1.amazonaws.com:5432/d65mct0s9rumev'
