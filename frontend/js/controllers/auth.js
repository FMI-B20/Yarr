yarr.controller('AuthController', ['$scope', 'AuthLogin', 'AuthRegister', 'Auth', 'Users', function ($scope, AuthLogin, AuthRegister, Auth, Users) {
  $scope.loginCredentials = {
    username: '',
    password: ''
  };
  $scope.registerCredentials = {
    username: '',
    password1: '',
    password2: '',
    email: ''
  };

  var loadUser = function() {
    Users.me().$promise.then(function(users) {
      Auth.setUser(users[0]);
    });
  };

  $scope.login = function (loginCredentials) {
    AuthLogin.login(loginCredentials, function(response) {
      Auth.setUser({ token: response.key });
      loadUser();
      alert('Logged in succesfully!');
    }, function() {
      alert('Unable to login due to incorect credentials!');
    });
  };
  $scope.register = function (registerCredentials) {
    AuthRegister.register(registerCredentials, function() {
      alert('Registration complete!');
      loadUser();
    }, function() {
      alert('Unable to register due to incorect credentials!');
    });
  };
}]);
