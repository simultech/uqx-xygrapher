var app = angular.module("app",['grapher','ngCookies']);
app.config(['$httpProvider','$interpolateProvider',function ($httpProvider,$interpolateProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    console.log("Configuring");
}]);