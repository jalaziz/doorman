from redmodel import models


class Message(models.Model):
    name = models.Attribute(indexed=True)
    message = models.Attribute()


class Group(models.Model):
    name = models.Attribute(indexed=True)
    message = models.ReferenceField(Message)
    contacts = models.SetField('Contact', indexed=True)


class Contact(models.Model):
    name = models.Attribute(indexed=True)
    pin = models.Attribute(unique=True)
    blacklisted = models.BooleanField(indexed=True)
    phone_number = models.Attribute(unique=True)
    group = models.ReferenceField(Group, indexed=True)
    message = models.ReferenceField(Message)


class Config(models.Model):
    name = models.Attribute(unique=True)
    value = models.Attribute()
