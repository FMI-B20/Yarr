from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
import json
from rest_framework.authtoken.models import Token

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

    phone_number1 = models.TextField(
        null = True,
        blank = False,
        validators = [RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")]
    )

    phone_number2 = models.TextField(
        null = True,
        blank = False,
        validators = [RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")]
    )

    image_url = models.URLField()

    location_types = models.ManyToManyField(LocationType)

    cuisines = models.ManyToManyField(Cuisine)

    location_lat = models.FloatField()
    location_lon = models.FloatField()

    @property
    def average_stars(self):
        return Rating.objects.filter(place=self.id).aggregate(Avg('stars')).values()[0]

    def __unicode__(self):
        return "[{}, {}, {}, {}, {}, {}, {}]".format(self.name, str(self.address), str(self.phone_number1), str(self.phone_number2), str(self.image_url), str(self.location_lat), str(self.location_lon))


class RecommandationHistory(models.Model):

    user = models.ForeignKey(User, null=True)
    time = models.DateTimeField(auto_now_add=True)

    location_types = models.ManyToManyField(LocationType)
    cuisines = models.ManyToManyField(Cuisine)

    location_lat = models.FloatField(null=True)
    location_lon = models.FloatField(null=True)
    radius = models.FloatField(null=True)

class Rating(models.Model):
    user = models.ForeignKey(User, null=True,blank=True)
    place = models.ForeignKey(Place)
    time = models.DateTimeField(auto_now_add=True)
    stars = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    commentary = models.TextField()

    class Meta:
        unique_together = (("user", "place"),)

    def __unicode__(self):
        return "[{}, {}]".format(unicode(self.user), unicode(self.place))
