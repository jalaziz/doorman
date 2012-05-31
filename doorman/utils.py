from flask import url_for
from twilio.twiml import Say, Sms, Play
from urlparse import urljoin

from doorman.config import config
import doorman.models as models


def grant_access(contact=None):
    verbs = []
    verbs.extend(message_actions(contact))
    verbs.extend(buzz_actions(config.buzz_code))
    
    try:
        notify = models.Group.objects.get(pk=config.notify)
    except models.Group.DoesNotExist:
        pass
    
    verbs.extend(notify_actions(notify, contact.name if contact else None))
    return verbs


def message_actions(contact):
    message = None
    contact_name = 'Sir or Madam'
    
    if contact:
        message = contact.message
        contact_name = contact.name
        if not message and contact.group:
            message = contact.group.message

    if not message:
        group = models.Group.objects.get(name='Default')
        message = group.message
    
    return Say(message % {'contact_name': contact_name})


def buzz_actions(code):
    return Play(dtmf_url(code))


def notify_actions(notify, contact_name=None):
    verbs = []
    
    message = '%s is coming.' % (contact_name or 'Someone')
    for contact in notify.contacts:
        verbs.append(Sms(message, to=contact.phone_number))
    
    return verbs


def dtmf_url(code):
    return urljoin(url_for('.static'), 'dtmf/%d.wav' % code)
