yarr.factory('Ratings', ['$resource', function($resource) {
  return $resource('/api/ratings/:id.json', { id: '@id' } , {
  	update: {
      method: 'PUT' // this method issues a PUT request
    }
  });
}]);