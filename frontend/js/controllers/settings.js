yarr.controller('SettingsController', ['$scope', 'Cuisines', function($scope, Cuisines) {
  $scope.cuisines = Cuisines.query();
}]);
