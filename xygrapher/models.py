"""
XYGrapher Models
"""

from mongoengine import *
import datetime

connect('project1')


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