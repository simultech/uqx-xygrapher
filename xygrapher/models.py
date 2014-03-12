"""
XYGrapher Models
"""
from django.conf import settings
from django.core import cache

from mongoengine import *
import datetime
from django.core.cache import cache

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
    def getsecretforkey(c_key):
        """
        Gets the consumer secret for the specified key
        :param c_key: the consumer key
        :return:the consumer secret
        """
        consumer = Consumer.objects(consumer_key=c_key).first()
        if consumer:
            return consumer.consumer_secret
        return "12345"


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
    def getall():
        """
        Gives back all existing plotpoints, caches the plotpoints
        :return: a list of all plotpoints
        """
        response_data = []
        if cache.get('plotpoint_cache'):
            response_data = cache.get('plotpoint_cache')
        else:
            existingcoords = Plotpoint.objects()
            for existingcoord in existingcoords:
                response_data.append({"x": existingcoord.x, "y": existingcoord.y})
            #Set the cache
            cache.set('plotpoint_cache', response_data, 30)
        return response_data

    @staticmethod
    def saveorupdate(obj, can_update="true"):
        """
        Either creates a new entry in the Plotpoint collection or updates the existing one based on the uid
        :param obj: a dict containing x,y and uid keys
        :param can_update: true or false whether it can update
        """
        existingcoord = Plotpoint.objects(uid=obj['uid']).first()
        if existingcoord:
            if can_update == "true":
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