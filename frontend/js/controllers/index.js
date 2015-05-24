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

  $scope.renderStars = function(value) {
    $('.rating').last().rating('create' , {disabled : true, showClear : false, size : 'sm', step : 0.1});
    $('.rating').last().rating('update', value);    
  };

}]);
