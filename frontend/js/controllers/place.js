yarr.controller('PlaceController', ['$scope', '$stateParams', 'Place', function($scope, $stateParams, Place) {
  $scope.place = Place.get({ id: $stateParams.id });
}]);
