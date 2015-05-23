from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route, list_route
from .serializers import UserSerializer, PlaceSerializer
from .serializers import RatingSerializer, CuisineSerializer, LocationTypeSerializer

from .models import Cuisine, Place, Rating, LocationType
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


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.DjangoFilterBackend]
    filter_fields = ['user', 'place']

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

    def get_queryset(self):
        cuisines_arg = self.request.QUERY_PARAMS.get('cuisines', None)
        types_arg = self.request.QUERY_PARAMS.get('locationtypes', None)
        recommended_queryset = Place.objects.all()

        if cuisines_arg is not None:
            cuisines_json_list = json.loads(cuisines_arg)
            if cuisines_json_list:
                recommended_queryset = recommended_queryset.filter(cuisines__pk__in = cuisines_json_list)            

        if types_arg is not None:
            types_json_list = json.loads(types_arg)
            if types_json_list:
                recommended_queryset = recommended_queryset.filter(location_types__pk__in = types_json_list)   
        
        return recommended_queryset
