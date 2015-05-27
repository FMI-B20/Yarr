yarr.factory('AuthInterceptor', ['Auth', function(Auth) {
  return {
    'request': function(config) {
      var token = Auth.token();
      if(token && token.length > 0 && token != 'null' && config.url.indexOf('/rest-auth/') !== 0) {
        config.headers.Authorization = "Token " + token;
      }
      return config;
    }
  };
}]);
