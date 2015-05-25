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
    lat : lat,
    lng : lng,
    radius : radius
  });

  
  $scope.loadMore = function() {
    $scope.loading = true;
    Recommandations.query({ 
      offset: $scope.recommendedPlaces.length,
      cuisines : JSON.stringify(cuisinesArr),
      locationTypes : JSON.stringify(locationTypesArr),
      lat : lat,
      lng : lng,
      radius : radius
    }).$promise.then(function(recommandations){
      [].push.apply($scope.recommendedPlaces, recommandations);
      $scope.loading = false;
    });
  };
}]);
