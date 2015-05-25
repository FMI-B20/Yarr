yarr.factory('Recommandations', ['$resource', function($resource) {
  return $resource('/api/recommend_places/:id.json', { id: '@id' });
}]);
