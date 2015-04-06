yarr.factory('Cuisines', ['djResource', function(djResource) {
  return djResource('/api/cuisines/.json');
}]);
