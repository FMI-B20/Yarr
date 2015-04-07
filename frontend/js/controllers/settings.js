yarr.controller('SettingsController', ['$scope', '$state', 'Cuisines', 'LocationTypes',
	function($scope, $state, Cuisines, LocationTypes) {

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

  	$state.go('recommend', {
      cuisines : cuisinesArr.join(','),
      locationTypes : locationTypesArr.join(',')
    });
  };
}]);
