yarr.controller('SettingsController', ['$scope', '$state', 'Cuisines', 'LocationTypes',
	function($scope, $state, Cuisines, LocationTypes) {

  $scope.bucharestLat = 44.4378258;
  $scope.bucharestLng = 26.0946376;

  $scope.$on('mapInitialized', function(event, map){

    $scope.map = map;
    
  })
  

  $scope.cuisines = Cuisines.query();
  $scope.locationTypes = LocationTypes.query();

	$scope.selectedCuisines = [];
	$scope.selectedLocationTypes = [];

  $scope.save = function() {

  	//selected cuisines
  	var cuisinesArr = [];
  	$.each($scope.selectedCuisines, function(index, cuisine) {
			cuisinesArr.push(cuisine.id);
  	});

  	//selected locationTypes
  	var locationTypesArr = [];
  	$.each($scope.selectedLocationTypes, function(index, locationType) {
			locationTypesArr.push(locationType.id);
  	});


    var circle = $scope.map.shapes[0];
    
    $state.go('recommend', {
      cuisines : cuisinesArr.join(','),
      locationTypes : locationTypesArr.join(','),
      lat : circle.getCenter().lat(),
      lng : circle.getCenter().lng(),
      radius : circle.getRadius()
    });
  };
}]);