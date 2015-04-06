yarr.controller('SettingsController', ['$scope', '$state', 'Cuisines', 'LocationTypes',
	function($scope, $state, Cuisines, LocationTypes) {
  
  $scope.cuisines = Cuisines.query();
  $scope.locationTypes = LocationTypes.query();

  $scope.save = function() {
  	
  	//selected cuisines
  	var cuisinesArr = [];
  	$.each($scope.cuisines, function(index, cuisine) {
  		
  		if(cuisine.selected && cuisine.selected == true)
  			cuisinesArr.push(cuisine.id);
  	});

  	//selected locationTypes
  	var locationTypesArr = [];
  	$.each($scope.locationTypes, function(index, locationType) {

  		if(locationType.selected && locationType.selected == true)
  			locationTypesArr.push(locationType.id);

  	});

  	// var newPath = "/places/cuisines/" + JSON.stringify(cuisinesArr) + "/locationTypes/" + JSON.stringify(locationTypesArr) + "/";

  	$state.go('recommend', {
      cuisines : cuisinesArr.join(','),
      locationTypes : locationTypesArr.join(',')
    });
  };
}]);
