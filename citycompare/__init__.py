#!venv/bin/python
from flask import Flask
import logging
import sys
import flask_bootstrap

flask_app = Flask(__name__)
flask_app.logger.addHandler(logging.StreamHandler(sys.stdout))
flask_app.logger.setLevel(logging.ERROR)
flask_app.config.from_object('config')
flask_app.config['SECRET_KEY'] = 'super-secret-key-that-noone-can-guess'
bootstrap = flask_bootstrap.Bootstrap(flask_app)
from citycompare import views
