yarr.controller('PlaceController', ['$scope', '$stateParams', '$state' , 'Places', 'Ratings', 'Users', 'Auth', function($scope, $stateParams, $state, Places, Ratings, Users, Auth) {
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
    place : $stateParams.id,
    user : null
  };

  $scope.initialRatingData = {
    stars : null,
    commentary : null,
    place : $stateParams.id, 
    user: null
  }

  if (Auth.user()) {
    $scope.ratingData.user = Auth.user().id;
    $scope.initialRatingData.user = Auth.user().id;
  }
  
  $scope.userHasRating = false;

  if ($scope.initialRatingData.user) {
    Ratings.query({place: $scope.initialRatingData.place, user: $scope.initialRatingData.user}).$promise.then(function(data) {
      if (data.length > 0) {
        $scope.userHasRating = true;
        $scope.ratingData.stars = data[0].stars;
        $scope.ratingData.commentary = data[0].commentary;
        $scope.initialRatingData.stars = data[0].stars;
        $scope.initialRatingData.commentary = data[0].commentary;
      }
    });
  }  

  $scope.submitRating = function() {
    var serializedRating = JSON.stringify($scope.ratingData);
    console.log(serializedRating);
    if ($scope.userHasRating) {
      Ratings.update(serializedRating).$promise.then(function(response) {
        alert('Rating updated!');
        $state.transitionTo($state.current, $stateParams, {
          reload: true,
          inherit: false,
          notify: true
        });
      }, function(error) {
        alert('Unable to update rating!');
      });
    } else {
      Ratings.save(serializedRating).$promise.then(function(response){
        alert('Rating submitted!');
        $state.transitionTo($state.current, $stateParams, {
          reload: true,
          inherit: false,
          notify: true
        });
      }, function(error) {
        alert('Unable to submit rating!');
      });
    }    
  };

  $scope.cancelWriteRating = function() {
    $scope.writeRating = false;
    $scope.ratingData.stars = $scope.initialRatingData.stars;
    $scope.ratingData.commentary = $scope.initialRatingData.commentary;
  };

}]);
