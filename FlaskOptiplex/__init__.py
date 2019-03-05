"""
The flask application package.
"""

from flask import Flask
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = 'thisisasecret'
lm = LoginManager(app)

import FlaskOptiplex.views
