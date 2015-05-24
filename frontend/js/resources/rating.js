yarr.factory('Place', ['djResource', function(djResource) {
  return djResource('/api/ratings/:id/.json', { id: '@id' });
}]);