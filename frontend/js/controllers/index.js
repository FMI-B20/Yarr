yarr.controller('IndexController', ['$scope', 'Place', function($scope, Place) {
  $scope.places = Place.query();
  $scope.loadMore = function() {
    $scope.loading = true;
    var page = Place.query({ offset: $scope.places.length }, function() {
      [].push.apply($scope.places, page);
      $scope.loading = false;
    });
  };
}]);
