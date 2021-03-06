yarr.factory('Auth', ['$cookies', function($cookies) {
  var Auth;
  
  var userCallbacks = [];
  var userNotify = function() {
    for(var i=0; i<userCallbacks.length; i++) {
      userCallbacks[i](Auth.user());
    }
  };

  Auth = {
    user: function() {
      var user = null;
      if ($cookies.user) {
        var user = JSON.parse($cookies.user);
      }
      if(user) {
        user.token = $cookies.token;
      }
      return user;
    },
    setUser: function(user) {
      $cookies.user = JSON.stringify(user);
      userNotify();
      return true;
    },
    setToken: function(token) {
      $cookies.token = token;
      userNotify();
    },
    token: function() {
      if ($cookies.token) {
        return $cookies.token;
      } else {
        return null;
      }
    },
    clear: function() {
      $cookies.user = null;
      $cookies.token = null;
      userNotify();
    },
    onUser: function(cb) {
      userCallbacks.push(cb);
      if($cookies.user || $cookies.token) {
        cb(Auth.user());
      }
    }
  };

  return Auth;
}]);
