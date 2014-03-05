angular.module('model',['ngCookies']).
	service('modelLoader',['$http','$q','$timeout','$cookies',function($http,$q,$timeout,$cookies) {
		
		this.load = function(url,data) {
			var httpRequest = {url:url};
			var method = 'GET';
			if(data) {
				method = 'POST';
                console.log("SENDING",data);
                httpRequest.data = $.param(data);
				httpRequest.headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'};
			}
			console.log("Loading");
			httpRequest.method = method;
			var delay = 10;
			var deferred = $q.defer();
			var obj = this;
			$timeout(function() {
				$http(httpRequest).
					success(function(data,status,headers,config) {
						deferred.resolve({'status':'success','data':data});
					}).
					error(function(data,status,headers,config) {
						deferred.resolve({'status':'error','data':data});
						throw new Error("Error loading"+url);
					})
			},delay);
			return deferred.promise;
		}
	}]);