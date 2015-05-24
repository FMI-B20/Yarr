from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route, list_route
from .serializers import UserSerializer, PlaceSerializer
from .serializers import RatingSerializer, CuisineSerializer, LocationTypeSerializer, MeSerializer
from main.models import User,Place,Rating,Cuisine,LocationType

import math
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    filter_backends = [filters.DjangoFilterBackend]

class MeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    serializer_class = MeSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.DjangoFilterBackend]
    filter_fields = ['user', 'place']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []

class LocationTypeViewSet(viewsets.ModelViewSet):
    queryset = LocationType.objects.all()
    serializer_class = LocationTypeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []

class RecomandationViewSet(viewsets.ModelViewSet):

    model = Place
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]

    def distance_meters(self, lat1, long1, lat2, long2):
 
        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi/180.0
             
        # phi = 90 - latitude
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians
             
        # theta = longitude
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
             
        # Compute spherical distance from spherical coordinates.
             
        # For two locations in spherical coordinates
        # (1, theta, phi) and (1, theta, phi)
        # cosine( arc length ) =
        #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length
         
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
               math.cos(phi1)*math.cos(phi2))
        arc = math.acos( cos )
     
        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.

        # we need the distance in meters (http://www.johndcook.com/blog/python_longitude_latitude/)
        return arc * 6373 * 1000

    def get_queryset(self):
        cuisines_arg = self.request.QUERY_PARAMS.get('cuisines', None)
        types_arg = self.request.QUERY_PARAMS.get('locationtypes', None)

        lat_arg = self.request.QUERY_PARAMS.get('lat', None)
        lng_arg = self.request.QUERY_PARAMS.get('lng', None)
        radius_arg = self.request.QUERY_PARAMS.get('radius', None)

        lat = float(json.loads(lat_arg))
        lng = float(json.loads(lng_arg))
        radius = float(json.loads(radius_arg))

        recommended_queryset = Place.objects.all()

        recommended_queryset = filter(lambda x: (self.distance_meters(lat, lng, float(x.location_lat), float(x.location_lon)) <= radius), recommended_queryset)
        
        if cuisines_arg is not None:
            cuisines_json_list = json.loads(cuisines_arg)
            if cuisines_json_list:
                recommended_queryset = recommended_queryset.filter(cuisines__pk__in = cuisines_json_list)

        if types_arg is not None:
            types_json_list = json.loads(types_arg)
            if types_json_list:
                recommended_queryset = recommended_queryset.filter(location_types__pk__in = types_json_list)

        return recommended_queryset
