yarr.config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise("/");

  $stateProvider
    .state('index', {
      url: "/",
      templateUrl: "/static/partials/index.html"
    })
    .state('recommend', {
      url: "/recommend/:cuisines/:locationTypes/",
      templateUrl: "/static/partials/recommend.html"
    })
    .state('place', {
      url: "/place/:id/",
      templateUrl: "/static/partials/place.html"
    })
    .state('profile', {
      url: "/profile/",
      templateUrl: "/static/partials/profile.html"
    })
    .state('settings', {
      url: "/settings/",
      templateUrl: "/static/partials/settings.html"
    })
    .state('login', {
      url: "/login",
      templateUrl: "/static/partials/login.html"
    })
	 .state('register', {
      url: "/register",
      templateUrl: "/static/partials/register.html"
    })
    .state('search', {
      url: "/s/:search/",
      templateUrl: "/static/partials/index.html"
    });
}]);
