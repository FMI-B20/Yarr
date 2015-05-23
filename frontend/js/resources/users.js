yarr.factory('Users', ['$resource', function($resource) {
  return $resource('/api/users/:action/.json', { }, {
    me: { method: 'GET', params: { action: 'me' }, isArray: true }
  });
}]);
