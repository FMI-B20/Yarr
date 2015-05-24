from rest_framework import serializers
from .models import Place, Rating, Cuisine, LocationType, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email', 'is_staff')

class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ('id','name')

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ('id','name')

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = (
            'id', 'name', 'address', 'phone_number1', 'phone_number2', 'location_types', 'cuisines',
            'location_lat', 'location_lon', 'image_url', 'average_stars'
        )


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'place', 'time', 'stars', 'commentary')
