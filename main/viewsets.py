from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route, list_route
from .serializers import UserSerializer, PlaceSerializer
from .serializers import RatingSerializer, CuisineSerializer, LocationTypeSerializer
from main.models import User,Place,Rating,Cuisine,LocationType

import math
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        queryset = Place.objects.all()

        if self.request.query_params.get('search'):
            search = self.request.query_params['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search)
            )

        return queryset

class MeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer

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

class RecomandationViewSet(viewsets.ReadOnlyModelViewSet):

    model = Place
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = []    

    def get_queryset(self):
        cuisines_arg = self.request.QUERY_PARAMS.get('cuisines', None)
        types_arg = self.request.QUERY_PARAMS.get('locationtypes', None)

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

        lat_arg = self.request.QUERY_PARAMS.get('lat', None)
        lng_arg = self.request.QUERY_PARAMS.get('lng', None)
        radius_arg = self.request.QUERY_PARAMS.get('radius', None)

        recommended_queryset = Place.objects.all()

        if cuisines_arg is not None:
            cuisines_json_list = json.loads(cuisines_arg)
            if cuisines_json_list:
                recommended_queryset = recommended_queryset.filter(cuisines__pk__in = cuisines_json_list)

        if types_arg is not None:
            types_json_list = json.loads(types_arg)
            if types_json_list:
                recommended_queryset = recommended_queryset.filter(location_types__pk__in = types_json_list)

        radius = 100
        
        if radius_arg is not None:
            try:
              radius = float(json.loads(radius_arg))
            except ValueError:
              pass

        if lat_arg is not None and lon_arg is not None:
            try:
                lat = float(json.loads(lat_arg))
                lng = float(json.loads(lng_arg))
                recommended_queryset = filter(lambda x: (distance_meters(lat, lng, float(x.location_lat), float(x.location_lon)) <= radius), recommended_queryset)
            except ValueError:
                pass      
        
        return recommended_queryset
