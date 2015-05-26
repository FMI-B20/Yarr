yarr.factory('Places', ['$resource', function($resource) {
  return $resource('/api/places/:id.json', { id: '@id' }, {
  	update: {
      method: 'PUT' // this method issues a PUT request
    }
  });
}]);