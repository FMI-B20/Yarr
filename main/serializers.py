from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Place, Rating, Cuisine, LocationType


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff')

class LocationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocationType
        fields = ('id','name')

class CuisineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cuisine
        fields = ('id','name')


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = (
            'id', 'name', 'address', 'phone_number1', 'phone_number2', 'location_types', 'cuisines', 
            'location_lat', 'location_lon', 'image_url'
        )
        depth = 1


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'place', 'time', 'rating', 'comentary')
        depth = 1
