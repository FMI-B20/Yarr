yarr.controller('LoginController', ['$scope', '$rootScope', '$http',function ($scope, $rootScope, $http) {
  $scope.credentials = {
    username: '',
    password: ''
  };
  $scope.login = function (credentials) {
	  
	  console.log($scope.credentials);
   $http.post('http://localhost:8000/rest-auth/login/').
  success(function(data, status, headers, config) {
	  console.log('a mers ',data);
    // this callback will be called asynchronously
    // when the response is available
  }).
  error(function(data, status, headers, config) {
	  console.log('eroare ',data);
    // called asynchronously if an error occurs
    // or server returns response with an error status.
  });
  /*  AuthService.login(credentials).then(function (user) {
      $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
      $scope.setCurrentUser(user);
    }, function () {
      $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
    });*/
  };
}]);



/*.constant('AUTH_EVENTS', {
  loginSuccess: 'auth-login-success',
  loginFailed: 'auth-login-failed',
  logoutSuccess: 'auth-logout-success',
  sessionTimeout: 'auth-session-timeout',
  notAuthenticated: 'auth-not-authenticated',
  notAuthorized: 'auth-not-authorized'
})

.constant('USER_ROLES', {
  all: '*',
  admin: 'admin',
  user: 'user',
  guest: 'guest'
})*/