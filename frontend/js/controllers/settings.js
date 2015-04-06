yarr.controller('SettingsController', ['$scope', 'Cuisines', 'LocationTypes', function($scope, Cuisines, LocationTypes) {
  
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
  	$.each($scope.locationTypesArr, function(index, locationType) {

  		if(locationType.selected && locationType.selected == true)
  			locationTypesArr.push(locationType.id);

  	});

  };
}]);
