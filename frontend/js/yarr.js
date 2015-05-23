var yarr = angular.module('yarr', [
  'ui.router', 'ui.bootstrap', 'ngResource', 'djangoRESTResources', 'ngMap', 'ui.select'
]);
yarr.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]).config(function($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});;
