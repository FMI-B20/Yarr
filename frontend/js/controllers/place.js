yarr.controller('PlaceController', ['$scope', '$stateParams', 'Places', 'Ratings', 'Users', function($scope, $stateParams, Places, Ratings, Users) {
  $scope.place = Places.get({ id: $stateParams.id });
  $scope.ratings = Ratings.query({ place: $stateParams.id, limit: 2 });
  $scope.ratings.$promise.then(function(ratings) {
    var functionForger = function(index) {
      return function(user) {
        ratings[index].username = user.username;
      }
    }
    for (var i = 0; i < ratings.length; i++) {
      var rating = ratings[i];
      Users.get({id : rating.user}).$promise.then(functionForger(i));
    }
  });

  $scope.loadMoreRatings = function() {
  	$scope.ratingsLoading = true;
    var page = Ratings.query({ offset: $scope.ratings.length, place: $stateParams.id });
    page.$promise.then(function(ratings) {
      var functionForger = function(index) {
        return function(users) {
          ratings[index].username = users.username;
        }
      }
      for (var i = 0; i < ratings.length; i++) {
        var rating = ratings[i];
        Users.get({id : rating.user}).$promise.then(functionForger(i));
      }
      $scope.ratingsLoading = false;
      [].push.apply($scope.ratings, ratings);
    });    
  }

  $scope.renderStars = function(value, id) {
    console.log(id);
    $('.rating').last().rating('create' , {disabled: true, showClear : false, size : 'sm', step : 1});
    $('.rating').last().rating('update', value);
  };

}]);
