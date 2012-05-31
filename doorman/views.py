from flask import request, render_template, url_for
from flask.views import MethodView
from twilio.twiml import Response

from doorman import doorman as app
from doorman.config import config
from doorman.decorators import twilio_view, register_api
from doorman.utils import grant_access
import doorman.models as models


@app.route('/')
def index():
    return render_template('doorman/index.html')


@app.route('/contacts/')
def contacts():
    return render_template('doorman/contacts.html')


@app.route('/config/')
def config():
    return render_template('doorman/config.html')


@app.route('/answer_call/')
@twilio_view
def answer_call():
    r = Response()
    
    if request.form['From'] != config.intercom:
        r.reject(reason='rejected')
    
    if not config.auth:
        r.verbs.extend(grant_access())
    else:
        with r.gather(action=url_for('.check_input'), numDigits=4, timeout=4) as g:
            g.say('Please enter a pin or hold.')
        
        try:
            contact = models.Contact.objects.get(pk=config.forward)
            r.dial(contact.phone_number)
        except models.Contact.DoesNotExist:
            pass
        
        r.say('Goodbye.')
    
    return r


@app.route('/check_input/')
@twilio_view
def check_input():
    r = Response()
    
    if request.form['Digits'] == config.master_pin:
        r.verbs.extend(grant_access())
    else:
        try:
            contact = models.Contact.objects.get(pin=request.form['Digits'])
        except models.Contact.DoesNotExist:
            contact = None
        
        if not contact or contact.blacklisted:
            r.say('Invalid pin code. Goodbye.')
        else:
            r.verbs.extend(grant_access(contact))
    
    return r


@register_api(app, 'contact_api', '/contacts/')
class ContactApi(MethodView):
    def get(self, id):
        if id is None:
            pass

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass


@register_api(app, 'group_api', '/groups/')
class GroupApi(MethodView):
    def get(self, id):
        if id is None:
            pass

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass


@register_api(app, 'config_api', '/config/', pk='name', pk_type='string')
class ConfigApi(MethodView):
    def get(self, name):
        if name is None:
            pass

    def post(self):
        pass

    def delete(self, name):
        pass

    def put(self, name):
        pass
