from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import UserSerializer, PlaceSerializer
from .serializers import RatingSerializer, CuisineSerializer, LocationTypeSerializer
from main.models import User, Place, Rating, Cuisine, LocationType, RecommandationHistory

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

    def retrieve(self, request, pk=None):
        return Response(status=403)

    def retrieve_last_query(self):
       all_hist = RecommandationHistory.objects.filter(user = self.request.user).order_by('time')

       #don't for what reason doesn't support negative index
       return all_hist[len(all_hist) - 1]

    def update_history(self, search_info):

        if self.request.user.is_anonymous():
            return 0

        last_query = self.retrieve_last_query()

        history_object = RecommandationHistory(
            user = self.request.user,
            location_lat = search_info['lat_arg'],
            location_lon = search_info['lng_arg'],
            radius = search_info['radius_arg'])

        history_object.save()

        cur_cuisines = set()
        cur_locations = set()

        if search_info['types_arg'] != None:
            loc_instances = LocationType.objects.filter(
                pk__in=search_info['types_arg']);

            for item in loc_instances:
                history_object.location_types.add(item)

            for item in loc_instances.values('name'):
                cur_cuisines.add(item['name'])

        if search_info['cuisines_arg'] != None:
            cuisine_instances = Cuisine.objects.filter(
                pk__in = search_info['cuisines_arg']);

            for item in cuisine_instances:
                history_object.cuisines.add(item)

            for item in cuisine_instances.values('name'):
                cur_cuisines.add(item['name'])

        
        last_locations = set(item.name for item in last_query.location_types.all())
        last_cuisines = set(item.name for item in last_query.cuisines.all())

        #print('last query ' + str(last_locations) + " " + str(last_cuisines))
        #print('cur query ' + str(cur_locations) + " " + str(cur_cuisines))

        if last_cuisines == cur_cuisines:
            if last_locations == cur_locations:
                #don't care, this query came from 'more results'
                history_object.delete()
                return 0

        history_object.save()
        #print('lala ' + str(int(search_info['cuisines_arg'][0])))

    def refine_set(self, recommended_queryset):
        recent_hist = RecommandationHistory.objects.filter(user = self.request.user).order_by('time')
        recent_hist = recent_hist[max(0, len(recent_hist) - 10):]

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
            scores[item] = cur_sum


        def compare_function(x, y):
            if scores[x] == scores[y]:
                avgx = x.average_stars
                avgy = y.average_stars

                if avgx == None:
                    agvx = 0.0
                if avgy == None:
                    avgy = 0.0

                if avgx < avgy:
                    return -1
                if avgx == avgy:
                    return 0
                if avgx > avgy:
                    return 1
            if scores[x] < scores[y]:
                return -1
            return 1

        recommended_queryset = sorted(recommended_queryset, cmp=compare_function, reverse=True)
        return recommended_queryset

    def get_queryset(self):

        cuisines_arg = self.request.QUERY_PARAMS.get('cuisines', None)
        types_arg = self.request.QUERY_PARAMS.get('locationtypes', None)

        def distance_meters(lat1, long1, lat2, long2): 
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

        self.update_history({
            'cuisines_arg': cuisines_json_list,
            'types_arg': types_json_list,
            'lat_arg': lat_arg,
            'lng_arg': lng_arg,
            'radius_arg': radius_arg
        })

        if lat_arg is not None and lng_arg is not None:
            try:
                lat = float(lat_arg)
                lng = float(lng_arg)
                recommended_queryset = filter(lambda x: (distance_meters(lat, lng, float(x.location_lat), float(x.location_lon)) <= radius), recommended_queryset)
            except ValueError:
                pass


        if self.request.user.is_anonymous() != True:
            recommended_queryset = self.refine_set(recommended_queryset)

        return recommended_queryset
