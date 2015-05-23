yarr.factory('Auth', ['$cookies', function($cookies) {
  return {
    user: function() {
      return $cookies.getObject('user');
    },
    setUser: function(user) {
      return $cookies.putObject('user', user);
    },
    token: function() {
      return $cookies.getObject('user').token;
    }
  };
}]);
