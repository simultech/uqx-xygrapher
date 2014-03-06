"""
XYGrapher Models
"""
from django.conf import settings

from mongoengine import *
import datetime

connect(settings.XYGRAPHER_MONGO_COLLECTION)

class Consumer(Document):
    """
    Model for OAuth keys
    """
    consumer_key = StringField(required=True)
    consumer_secret = StringField(required=True)

    @staticmethod
    def validconsumer(consumer_key, consumer_secret):
        """
        Checks whether a consumer is valid
        :param consumer_key: the consumer key
        :param consumer_secret: the consumer secret
        :return:true or false
        """
        consumer = Consumer.objects(consumer_key=consumer_key).first()
        if consumer:
            if consumer.consumer_secret == consumer_secret:
                return True
        return False

    @staticmethod
    def getsecretforkey(consumer_key):
        """
        Gets the consumer secret for the specified key
        :param consumer_key: the consumer key
        :return:the consumer secret
        """
        consumer = Plotpoint.objects(consumer_key=consumer_key).first()
        if consumer:
            return consumer.consumer_secret
        return ""

class Plotpoint(Document):
    """
    Model for saving MongoDB Plotpoints
    """
    uid = StringField(required=True)
    x = FloatField()
    y = FloatField()
    created_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def saveorupdate(obj):
        """
        Either creates a new entry in the Plotpoint collection or updates the existing one based on the uid
        :param obj: a dict containing x,y and uid keys
        """
        existingcoord = Plotpoint.objects(uid=obj['uid']).first()
        if existingcoord:
            existingcoord.x = obj['x']
            existingcoord.y = obj['y']
            existingcoord.modified_date = datetime.datetime.now
            existingcoord.save()
        else:
            newcoord = Plotpoint(obj['uid'])
            newcoord.x = obj['x']
            newcoord.y = obj['y']
            newcoord.created_date = datetime.datetime.now
            newcoord.modified_date = datetime.datetime.now
            newcoord.save()