yarr.controller('HeaderController', ['$scope', '$state', 'Auth', 'Users', function($scope, $state, Auth, Users) {
  Auth.onUser(function(user) {
    console.log(user);
    $scope.user = user;
  });
  Users.me().$promise.then(function(users) {
    Auth.setUser(users[0]);
  });

  $scope.logout = function() {
    Auth.clear();
    $state.go('index');
  };
}]);
