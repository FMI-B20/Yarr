yarr.controller('HeaderController', ['$scope', 'Auth', 'Users', function($scope, Auth, Users) {
  Auth.onUser(function(user) {
    $scope.user = user;
    console.log(user);
  });
  Users.me().$promise.then(function(users) {
    Auth.setUser(users[0]);
  });

  $scope.logout = function() {
    Auth.clear();
  };
}]);
