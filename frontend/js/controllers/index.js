yarr.controller('IndexController', ['$scope', 'Place', function($scope, Place) {
  var currentPage = 1;

  $scope.places = Place.query({ page: currentPage });
  $scope.loadMore = function() {
    $scope.loading = true;
    currentPage ++;
    var page = Place.query({ page: currentPage }, function() {
      [].push.apply($scope.places, page);
      $scope.loading = false;
    });
  };
}]);
