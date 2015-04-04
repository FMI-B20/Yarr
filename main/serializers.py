from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Place, Visit, Cuisine, LocationType


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff')

class LocationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocationType
        fields = ('name',)

class CuisineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cuisine
        fields = ('name',)


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Place
        fields = (
            'id', 'name', 'address', 'location_types', 'cuisines',
            'location_lat', 'location_lon'
        )
        depth = 1


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    place = PlaceSerializer()

    class Meta:
        model = Visit
        fields = ('id', 'user', 'place', 'time', 'rating')
