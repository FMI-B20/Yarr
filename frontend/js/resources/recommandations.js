yarr.factory('Recommandations', ['djResource', function(djResource) {
  return djResource('/api/recommend_places/?cuisines=:cuisines&locationtypes=:locationTypes', {}, {});
}]);
