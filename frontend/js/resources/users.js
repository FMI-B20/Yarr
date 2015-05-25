yarr.factory('Users', ['$resource', function($resource) {
  return $resource('/api/users/:action:id.json', { id: '@id' }, {
    me: { method: 'GET', params: { action: 'me' }, isArray: true }
  });
}]);
