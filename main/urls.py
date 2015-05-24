from django.conf.urls import url, include
from rest_framework import routers
from .viewsets import UserViewSet, PlaceViewSet, RatingViewSet, CuisineViewSet, LocationTypeViewSet, RecomandationViewSet, MeViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users/me', MeViewSet, "Me")
router.register(r'users', UserViewSet)
router.register(r'places', PlaceViewSet, "Place")
router.register(r'ratings', RatingViewSet)
router.register(r'cuisines', CuisineViewSet)
router.register(r'location_types', LocationTypeViewSet)
router.register(r'recommend_places', RecomandationViewSet, "Place")

urlpatterns = [
    url(r'^', include(router.urls)),
]
