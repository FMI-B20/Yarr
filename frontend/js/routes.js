yarr.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/");

  $stateProvider
    .state('index', {
      url: "/",
      templateUrl: "/static/partials/index.html"
    })
    .state('places', {
      url: "/places/",
      templateUrl: "/static/partials/places.html"
    })
    .state('place', {
      url: "/place/:id/",
      templateUrl: "/static/partials/place.html"
    })
    .state('settings', {
      url: "/settings/",
      templateUrl: "/static/partials/settings.html"
    });
}]);
