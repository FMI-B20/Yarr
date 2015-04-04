var yarr = angular.module('yarr', ['ui.router', 'ui.bootstrap', 'ngResource', 'djangoRESTResources', 'ngMap']);
yarr.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);
