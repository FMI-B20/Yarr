yarr.controller('RecommendController', ['$scope', '$stateParams', 'Recommandations',
    function($scope, $stateParams, Recommandations) {
  
  var cuisinesArr = $stateParams.cuisines.split(',');
  var locationTypesArr = $stateParams.locationTypes.split(',');

  $.each(cuisinesArr, function(index, val) {
  	 cuisinesArr[index] = parseInt(val);
  });

  $.each(locationTypesArr, function(index, val) {
  	 locationTypesArr[index] = parseInt(val);
  });
  
  $scope.recommendedPlaces = Recommandations.query({
  	cuisines : JSON.stringify(cuisinesArr),
  	locationTypes : JSON.stringify(locationTypesArr)
  });

}]);
