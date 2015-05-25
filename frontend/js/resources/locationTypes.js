yarr.factory('LocationTypes', ['$resource', function($resource) {
  return $resource('/api/location_types/:id.json', { id: '@id' });
}]);
