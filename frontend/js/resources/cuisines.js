yarr.factory('Cuisines', ['$resource', function($resource) {
  return $resource('/api/cuisines/:id.json', { id: '@id' });
}]);
