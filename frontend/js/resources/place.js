yarr.factory('Place', ['$resource', function($resource) {
  return $resource('/api/places/:id.json', { id: '@id' });
}]);
