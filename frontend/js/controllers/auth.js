yarr.controller('AuthController', ['$scope', '$location' , 'AuthLogin', 'AuthRegister', 'Auth', 'Users', function ($scope, $location, AuthLogin, AuthRegister, Auth, Users) {

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

  $scope.login = function (loginCredentials) {
    AuthLogin.login(loginCredentials).$promise.then(function(response) {
      Auth.setToken(response.key);
      Users.me().$promise.then(function(users) { Auth.setUser(users[0]); });
      alert('Logged in succesfully!');
      $location.path('/');
    }, function(error) {
      alert('Unable to login due to incorect credentials!');
    });
  };

  $scope.register = function (registerCredentials) {
    AuthRegister.register(registerCredentials).$promise.then(function(response) {
      alert('Registration complete!');
      $scope.login({username : registerCredentials.username, password : registerCredentials.password1});
    }, function(error) {
      alert('Unable to register due to incorect credentials!');
    });
  };
}]);
