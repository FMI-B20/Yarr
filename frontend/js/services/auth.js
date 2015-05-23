yarr.factory('Auth', ['$cookies', function($cookies) {
  return {
    user: function() {
      return $cookies.user;
    },
    setUser: function(user) {
      return ($cookies.user = JSON.stringify(user));
    },
    token: function() {
      try {
        return JSON.parse($cookies.user).token;
      } catch(e) {
        return null;
      }
    }
  };
}]);
