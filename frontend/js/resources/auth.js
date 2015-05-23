yarr.factory('AuthLogin', ['$resource', function($resource) {
  return $resource('/rest-auth/login/', {}, {
    login: { method: 'POST' }
  });
}]);

yarr.factory('AuthRegister', ['$resource', function($resource) {
  return $resource('/rest-auth/registration/', {},{
    register: { method: 'POST' }
  });
}]);
