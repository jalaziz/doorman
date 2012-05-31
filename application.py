#!/usr/bin/env python

from flask import Flask
from doorman import doorman

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(doorman)

if __name__ == '__main__':
    app.run(debug=True)
