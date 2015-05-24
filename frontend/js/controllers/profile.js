yarr.controller('ProfileController', ['$scope', 'Auth', function($scope, Auth) {
  Auth.onUser(function(user) {
    $scope.user = user;
  });
}]);
