yarr.factory('Cuisines', ['$resource', function($resource) {
  return $resource('/api/cuisines/:id.json', { id: '@id' }, {
  	update: {
      method: 'PUT' // this method issues a PUT request
    }
  });
}]);
