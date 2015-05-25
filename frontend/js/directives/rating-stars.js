yarr.directive('ratingStarsOptions', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            $(element).rating('create', scope.$eval(attrs.ratingStarsOptions));
        }
    };
});

yarr.directive('ratingStarsValue', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            $(element).rating('update', attrs.ratingStarsValue);
        }
    };
});

yarr.directive('ratingStarsOnRatingChange', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            $(element).on('rating.change', scope.$eval(attrs.ratingStarsOnRatingChange));
        }
    };
});