"""
This script runs the FlaskOptiplex application using a development server.
"""

from os import environ
from FlaskOptiplex import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '192.168.1.109')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
