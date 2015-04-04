yarr.factory('Place', ['djResource', function(djResource) {
  return djResource('/api/places/:id/.json', { id: '@id' });
}]);
