yarr.directive('ratingStarsOptions', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            $(element).rating('create', scope.$eval(attrs.ratingStarsOptions));
            $(element).rating('update', attrs.ratingStarsValue);
        }
    };
});