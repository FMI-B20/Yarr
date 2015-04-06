yarr.controller('SettingsController', ['$scope', 'Cuisines', 'LocationTypes', '$location', 
	function($scope, Cuisines, LocationTypes, $location) {
  
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

  	var newPath = "/places/cuisines/" + JSON.stringify(cuisinesArr) + "/locationTypes/" + JSON.stringify(locationTypesArr) + "/";

  	$location.path(newPath);
  };
}]);
