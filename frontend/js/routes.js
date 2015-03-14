yarr.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/");

    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/partials/index.html"
        }).state('places', {
            url: "/places/",
            templateUrl: "/static/partials/places.html"
        });
}]);