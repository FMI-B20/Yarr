yarr.controller('IndexController', ['$scope', '$state', '$stateParams', 'Place', function($scope, $state, $stateParams, Place) {
  $scope.searchTerm = $stateParams.search;
  $scope.places = Place.query({ search: $stateParams.search });
  $scope.loadMore = function() {
    $scope.loading = true;
    var page = Place.query({ offset: $scope.places.length, search: $stateParams.search }, function() {
      [].push.apply($scope.places, page);
      $scope.loading = false;
    });
  };

  $scope.search = function() {
    $state.go('search', { search: $scope.searchTerm });
  };
}]);
