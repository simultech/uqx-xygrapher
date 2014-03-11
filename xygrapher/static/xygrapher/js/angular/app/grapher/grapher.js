var grapher = angular.module("grapher",['model']);

grapher.controller('GrapherCtrl',['$scope','modelLoader',function($scope, modelLoader) {
	
	//graph data
	$scope.data = {};
	
	//states
	$scope.items = ['unavailable','not_entered','entered'];
	$scope.state = $scope.items[0];
	
	//student ID
	$scope.student_id = "";
	$scope.x_value_val = "";
	$scope.y_value_val = "";

    //setup variables
    $scope.x_axis_label = "asdf";
    $scope.y_axis_label = "fghj";
    $scope.min_x_value = null;
    $scope.min_y_value = null;
    $scope.max_x_value = null;
    $scope.max_y_value = null;
    $scope.showlines = false;
    $scope.multiple_attempts = "true";
    $scope.require_grade = "true";
    $scope.submit_button = "edit values";
    $scope.can_resubmit = false;
	
	//URLs
	$scope.getdataURL = '/grapher/xygrapher/data/';
	$scope.submitURL = '/grapher/xygrapher/savecoord/';
	
	//Start the app
	$scope.$watch('student_id',function(newVal,oldVal) {
		console.log($scope.student_id);
		init();
	});
	
	$scope.submitGrade = function () {
        //get the x and y value
        $scope.x_value_val = parseFloat(angular.element("#x_value").val());
        if($scope.x_value_val == NaN) {
            $scope.x_value_val = 0;
        }
        $scope.y_value_val = parseFloat(angular.element("#y_value").val());
        if($scope.y_value_val == NaN) {
            $scope.y_value_val = 0;
        }
        //send the x and y value to the server
        modelLoader.load($scope.submitURL, {'x': $scope.x_value_val, 'y': $scope.y_value_val, 'uid': $scope.student_id}).then(function (response) {
            if (response.status == 'success') {
                //set data and change state
                if (response.data.saved == 'true') {
                    setState();
                } else {
                    //show an error
                }
            } else {
                //show an error
            }
        });
    };
	
	$scope.editGrade = function () {
        $scope.state = 'not_entered';
    };
	
	//Check initial state
	function init() {
		//check if the student has submitted previously
		setState();
	}
	
	function setState() {
		modelLoader.load($scope.getdataURL).then(function(response) {
			if(response.status == 'success') {
				var submitted = response.data.entered;
				if(submitted == "true" || $scope.require_grade == 'false') {
                    if(submitted == "true") {
    					$scope.x_value_val = response.data.current_x;
	    				$scope.y_value_val = response.data.current_y;
                        if($scope.multiple_attempts == 'true') {
                            $scope.can_resubmit = true
                        } else {
                            $scope.can_resubmit = false
                        }
                    } else {
                        $scope.can_resubmit = true
                    }
					//show graph
					$scope.state = 'entered';
					//set data
					$scope.data = response.data.data;
				} else {
					//show input
					$scope.state = 'not_entered';
                    console.log("Going to edit")
				}
			} else {
				//show an error
			}
		});
	}
}]);