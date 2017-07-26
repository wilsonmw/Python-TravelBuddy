from __future__ import unicode_literals

from django.db import models

from ..login_app.models import User
import datetime

# Create your models here.
class TripManager(models.Manager):
    def addNewTrip(self, postData, id):
        results = {'status':True, 'errors':[]}      
        if not postData['destination'] or len(postData['destination'])<3:
            results['status']=False
            results['errors'].append("Travel Destination must be at least 3 characters.")
        if not postData['description'] or len(postData['description'])<3:
            results['status']=False
            results['errors'].append("Travel Description must be at least 3 characters.")
        if not postData['beginDate'] or not postData['endDate']:
            results['status']=False
            results['errors'].append("You must enter start and end dates for your trip.")
        else:
            user = User.objects.get(id=id)
            Trip.objects.create(destination = postData['destination'], description = postData['description'], beginDate = postData['beginDate'], endDate=postData['endDate'], owner = user)
            return results
        return results

    def join(self, tripId, userId):
        trip = Trip.objects.get(id=tripId)
        user = User.objects.get(id = userId)
        trip.joins.add(user)
        trip.save()
        return trip

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.TextField()
    beginDate = models.DateField()
    endDate = models.DateField()
    owner = models.ForeignKey(User)
    joins = models.ManyToManyField(User, related_name='joins')
    objects = TripManager()
