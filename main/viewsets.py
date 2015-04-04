from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, PlaceSerializer
from .serializers import VisitSerializer, CuisineSerializer, LocationTypeSerializer
from .models import Cuisine, Place, Visit, LocationType


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer


class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer


class LocationTypeViewSet(viewsets.ModelViewSet):
	queryset = LocationType.objects.all()
	serializer_class = LocationTypeSerializer
