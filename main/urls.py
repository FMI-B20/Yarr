from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import UserViewSet, PlaceViewSet, VisitViewSet, CuisineViewSet, LocationTypeViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'cuisines', CuisineViewSet)
router.register(r'location_types', LocationTypeViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
