import flask

doorman = flask.Blueprint('doorman', __name__,  static_folder='static', template_folder='templates')

import doorman.views
