yarr.factory('AuthInterceptor', ['Auth', function(Auth) {
  return {
    'request': function(config) {
      var token = Auth.token();
      if(token && token.length > 0 && token != 'null') {
        config.headers.Authorization = "Token " + token;
      }
      return config;
    }
  };
}]);
