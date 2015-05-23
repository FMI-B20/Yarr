yarr.controller('AuthController', ['$scope', 'AuthLogin', 'AuthRegister', function ($scope, AuthLogin, AuthRegister) {
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
    AuthLogin.login(JSON.stringify(loginCredentials), function(){
      alert('Logged in succesfully!');
    }, function(){
      alert('Unable to login due to incorect credentials!');
    });
  };
  $scope.register = function (registerCredentials) {
    console.log(JSON.stringify(registerCredentials));
    AuthRegister.register(JSON.stringify(registerCredentials), function(){
      alert('Registration complete!');
    }, function(){
      alert('Unable to register due to incorect credentials!');
    });
  };
}]);
