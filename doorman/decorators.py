from flask import abort, current_app, request, make_response
from functools import wraps
from twilio.util import RequestValidator
from twilio.twiml import Verb


def twilio_view(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_app.config['DEBUG']:
            validator = RequestValidator(current_app.config['TWILIO_AUTH_TOKEN'])
            if not validator.validate(request.url, request.form, request.headers['HTTP_X_TWILIO_SIGNATURE']):
                abort(401)
        response = f(*args, **kwargs)
        if isinstance(response, Verb):
            response = str(response)
        response = make_response(response)
        response.mimetype = 'application/xml'
        return response
    return decorator()


def register_api(app, endpoint, url, pk='id', pk_type='int', prefix='/api'):
    def cls_wrapper(cls):
        view_func = cls.as_view(endpoint)
        url = '%s%s' % (prefix, url)
        app.add_url_rule(url, defaults={pk: None},
                         view_func=view_func, methods=['GET',])
        app.add_url_rule(url, view_func=view_func, methods=['POST',])
        app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                         methods=['GET', 'PUT', 'DELETE'])
    return cls_wrapper
