yarr.factory('AuthInterceptor', ['Auth', function(Auth) {
  return {
    'request': function(config) {
      var token = Auth.token();
      if(token) {
        config.headers.Authorization = "Token " + token;
      }
      return config;
    }
  };
}]);
