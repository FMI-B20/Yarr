yarr.factory('Cuisines', ['$resource', function($resource) {
  return $resource('/api/cuisines.json');
}]);
