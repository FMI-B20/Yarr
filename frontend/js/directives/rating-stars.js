yarr.directive('ratingstars', function($parse){
    return {
        restrict: 'E',
        compile: function(element,attrs) {

        	var modelAccessor = $parse(attrs.ngModel);
        	//angular.element(element).rating('create');

        	// linking function here.
	      	return function(scope,elem,attrs) {
	        	angular.element(elem).rating('create', {disabled: attrs.inputDisabled == "true", showClear : attrs.showClear == "true", size : attrs.size, step : attrs.step, min : attrs.min, max : attrs.max});
            	scope.$watch(modelAccessor, function (value) {
               		angular.element(elem).rating('update', value);
            	});
            	angular.eleelementm(elem).on('rating.change', function(event, value, caption) {
            		modelAccessor.assign(scope, value);
            	});
	      	};
	    }
    };
});