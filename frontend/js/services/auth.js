yarr.factory('Auth', ['$cookies', function($cookies) {
  var userCallbacks = [];
  var userNotify = function() {
    for(var i=0; i<userCallbacks.length; i++) {
      userCallbacks[i](JSON.parse($cookies.user));
    }
  };

  var Auth = {
    user: function() {
      return JSON.parse($cookies.user);
    },
    setUser: function(user) {
      $cookies.user = JSON.stringify(user);
      userNotify();
      return true;
    },
    token: function() {
      try {
        return JSON.parse($cookies.user).token;
      } catch(e) {
        return null;
      }
    },
    clear: function() {
      $cookies.user = null;
      userNotify();
    },
    onUser: function(cb) {
      userCallbacks.push(cb);
    }
  };

  return Auth;
}]);
