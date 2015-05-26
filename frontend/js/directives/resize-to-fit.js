yarr.directive('resizeToFit', function ($window) {
    return function (scope, element) {
        var w = angular.element($window);
        var changeHeight = function() { 
        	element.css('min-height', (w.height() -20) + 'px' );
        };  
        w.bind('resize', function () {        
              changeHeight();   // when window size gets changed             
        });  
        changeHeight(); // when page loads          
    }
});