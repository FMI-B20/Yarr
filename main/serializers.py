from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Place, Visit, Cuisine


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff')


class CuisineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cuisine
        fields = ('name',)


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    cuisine = CuisineSerializer()

    class Meta:
        model = Place
        fields = (
            'id', 'name', 'address', 'location_type', 'cuisine', 
            'location_lat', 'location_lon'            
        )


class VisitSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    place = PlaceSerializer()

    class Meta:
        model = Visit
        fields = ('id', 'user', 'place', 'time', 'rating')