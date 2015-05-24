yarr.controller('RecommendController', ['$scope', '$stateParams', 'Recommandations',
    function($scope, $stateParams, Recommandations) {
  
  var cuisinesArr = [];
  if($stateParams.cuisines != "")
    cuisinesArr = $stateParams.cuisines.split(',');
  
  var locationTypesArr = [];
  if($stateParams.locationTypes != "")
    locationTypesArr = $stateParams.locationTypes.split(',');

  $.each(cuisinesArr, function(index, val) {
  	 cuisinesArr[index] = parseInt(val);
  });

  $.each(locationTypesArr, function(index, val) {
  	 locationTypesArr[index] = parseInt(val);
  });
  
  var lat = $stateParams.lat;
  var lng = $stateParams.lng;
  var radius = $stateParams.radius;

  $scope.recommendedPlaces = Recommandations.query({
  	cuisines : JSON.stringify(cuisinesArr),
  	locationTypes : JSON.stringify(locationTypesArr),
    lat : JSON.stringify(lat),
    lng : JSON.stringify(lng),
    radius : JSON.stringify(radius)
  });

  
  $scope.loadMore = function() {
    $scope.loading = true;
    var page = Recommandations.query({ 
      offset: $scope.recommendedPlaces.length,
      cuisines : JSON.stringify(cuisinesArr),
      locationTypes : JSON.stringify(locationTypesArr),
      lat : JSON.stringify(lat),
      lng : JSON.stringify(lng),
      radius : JSON.stringify(radius)
    }, function() {
      [].push.apply($scope.recommendedPlaces, page);
      $scope.loading = false;
    });
  };

}]);
