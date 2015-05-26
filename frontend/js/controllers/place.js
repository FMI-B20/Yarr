yarr.controller('PlaceController', ['$scope', '$timeout', '$stateParams', 'Places', 'Ratings', 'Users', function($scope, $timeout, $stateParams, Places, Ratings, Users) {
  $scope.place = Places.get({ id: $stateParams.id });
  $scope.ratings = Ratings.query({ place: $stateParams.id });
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

  $scope.writeRating = false;
  $scope.ratingData = {
    stars : null,
    commentary : null,
    place : $stateParams.id
  };
  $scope.userHasRating = false;

  Ratings.query({place: $stateParams.id, user: 2}).$promise.then(function(data) {
    if (data.length > 0) {
      $scope.userHasRating = true;
      $scope.ratingData = data[0];
      console.log($scope.ratingData);
    }
  });

  $scope.submitRating = function() {
    var serializedRating = JSON.stringify($scope.ratingData);
    console.log(serializedRating);
    Ratings.save(serializedRating).$promise.then(function(response){
      alert('Rating submitted!');
    }, function(error) {
      alert('Unable to submit rating!');
    });
  };

}]);
