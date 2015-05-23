yarr.factory('AuthLogin', ['djResource', function(djResource) {
  return djResource(
    '/rest-auth/login/', 
    {}, 
    {
        login: { method: 'POST' }
    });
}]);

yarr.factory('AuthRegister', ['djResource', function(djResource) {
  return djResource(
    '/rest-auth/registration/', 
    {}, 
    {
        register: { method: 'POST' }
    });
}]);