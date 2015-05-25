yarr.controller('IndexController', ['$scope', '$state', '$stateParams', 'Places', function($scope, $state, $stateParams, Places) {
  $scope.searchTerm = $stateParams.search;
  $scope.places = Places.query({ search: $stateParams.search });
  $scope.loadMore = function() {
    $scope.loading = true;
    var page = Places.query({ offset: $scope.places.length, search: $stateParams.search });
    page.$promise.then(function(places) {
      [].push.apply($scope.places, places);
      $scope.loading = false;
    });
  };

  $scope.search = function() {
    $state.go('search', { search: $scope.searchTerm });
  };

  $scope.renderStars = function(value) {
    $('.rating').last().rating('create' , {disabled: true, showClear : false, size : 'sm', step : 0.1});
    $('.rating').last().rating('update', value);
  };

}]);
