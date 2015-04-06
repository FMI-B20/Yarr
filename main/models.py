from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

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

    image_url = models.URLField(
        null = True, 
        blank = False
    )
    
    location_types = models.ManyToManyField(LocationType)

    cuisines = models.ManyToManyField(Cuisine)
    
    location_lat = models.FloatField()
    location_lon = models.FloatField()

    def __unicode__(self):
        return ''.join(["(",", ".join(
            [
            self.name, 
            str(self.phone_number1), 
            str(self.phone_number2), 
            str(self.image_url),
            str(self.location_lat), 
            str(self.location_lon)
            ]
        ),")"])


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