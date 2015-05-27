from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import UserSerializer, PlaceSerializer
from .serializers import RatingSerializer, CuisineSerializer, LocationTypeSerializer
from main.utils import IsStaffOrReadOnly
from main.models import User,Place,Rating,Cuisine,LocationType,RecommandationHistory

import math
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaffOrReadOnly]
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
    permission_classes = [IsStaffOrReadOnly]

class RecomandationViewSet(viewsets.ReadOnlyModelViewSet):

    model = Place
    serializer_class = PlaceSerializer
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, pk=None):
        return Response(status=403)

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

    def update_history(self, search_info):

        if self.request.user.is_anonymous():
            return 0

        history_object = RecommandationHistory(
            user = self.request.user,
            location_lat = search_info['lat'],
            location_lon = search_info['lng'],
            radius = search_info['radius'])

        all_history = RecommandationHistory.objects.filter(user = self.request.user).order_by('-time')       

        if not all_history:
            history_object.save()
            return 1

        last_history_object = all_history[0]        

        cur_cuisines = set()
        cur_locations = set()

        if search_info['location_types'] != None:
            loc_instances = LocationType.objects.filter(
                pk__in=search_info['location_types']);

            for item in loc_instances:
                history_object.location_types.add(item)
                cur_locations.add(item.name)

        if search_info['cuisines'] != None:
            cuisine_instances = Cuisine.objects.filter(
                pk__in = search_info['cuisines']);

            for item in cuisine_instances:
                history_object.cuisines.add(item)
                cur_cuisines.add(item.name)
        
        last_locations = set(item.name for item in last_history_object.location_types.all())
        last_cuisines = set(item.name for item in last_history_object.cuisines.all())

        if last_cuisines == cur_cuisines:
            if last_locations == cur_locations:
                if history_object.location_lat == last_history_object.location_lat:
                    if self.distance_meters(last_history_object.location_lat, last_history_object.location_lon, history_object.location_lat, history_object.location_lon) < 1:
                        if last_history_object.radius == history_object.radius:
                            #don't care, this query came from 'more results'
                            print "The same"
                            return 0

        history_object.save()
        return 1

    def refine_set(self, recommended_queryset, k_threshold):
        recent_hist = RecommandationHistory.objects.filter(user = self.request.user).order_by('time')
        recent_hist = recent_hist[max(0, len(recent_hist) - k_threshold):]

        recent_hist.reverse()

        cache = dict()

        for item in recent_hist:
            all_cuisines = item.cuisines.all()
            all_locations = item.location_types.all()
            for cuis in all_cuisines:
                if cuis.name not in cache.keys():
                    cache[cuis.name] = 1
                else:
                    cache[cuis.name] += 1

            for loc in all_locations:
                if loc.name not in cache.keys():
                    cache[loc.name] = 1
                else:
                    cache[loc.name] += 1

        scores = dict()

        for item in recommended_queryset:

            cur_sum = 0
            for cuisine in item.cuisines.all():
                if cuisine.name in cache.keys():
                    cur_sum += cache[cuisine.name]

            avg = item.average_stars

            if avg is None:
                avg = 3.0

            scores[item] = avg * cur_sum

        def compare_function(x, y):
            if scores[x] == scores[y]:
                return 0
            if scores[x] < scores[y]:
                return -1
            return 1

        recommended_queryset = sorted(recommended_queryset, cmp=compare_function, reverse=True)
        #print([scores[item] for item in recommended_queryset])
        return recommended_queryset

    def get_queryset(self):

        cuisines_arg = self.request.QUERY_PARAMS.get('cuisines', None)
        types_arg = self.request.QUERY_PARAMS.get('locationtypes', None)        

        lat_arg = self.request.QUERY_PARAMS.get('lat', None)
        lng_arg = self.request.QUERY_PARAMS.get('lng', None)
        radius_arg = self.request.QUERY_PARAMS.get('radius', None)


        recommended_queryset = Place.objects.all()

        cuisines_json_list = None
        types_json_list = None

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
              radius = float(radius_arg)
            except ValueError:
              pass

        history_info = {
            'cuisines': cuisines_json_list,
            'location_types': types_json_list,
            'lat': None,
            'lng': None,
            'radius': radius
        }

        if lat_arg is not None and lng_arg is not None:
            try:
                lat = float(lat_arg)
                lng = float(lng_arg)
                recommended_queryset = filter(lambda x: (self.distance_meters(lat, lng, float(x.location_lat), float(x.location_lon)) <= radius), recommended_queryset)
                history_info['lat'] = lat;
                history_info['lng'] = lng;
            except ValueError:
                pass

        self.update_history(history_info)

        if self.request.user.is_anonymous() != True:
            #take the last 30 recommandations
            recommended_queryset = self.refine_set(recommended_queryset, 30)
        else:
            recommended_queryset = sorted(recommended_queryset, key=lambda x: x.average_stars, reverse = True)

        return recommended_queryset
