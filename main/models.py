from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Cuisine(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

class LocationType(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField()
    
    location_types = models.ManyToManyField(LocationType)

    cuisines = models.ManyToManyField(Cuisine)
    
    location_lat = models.FloatField()
    location_lon = models.FloatField()

    def __unicode__(self):
        return self.name


class Visit(models.Model):
    user = models.ForeignKey(User)
    place = models.ForeignKey(Place)
    time = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True
    )

    def __unicode__(self):
        return "[{}, {}]".format(unicode(self.user), unicode(self.place))