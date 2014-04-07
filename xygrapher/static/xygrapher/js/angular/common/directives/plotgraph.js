app.directive("plotgraph",function($window) {
	
	var xAxisName = "X Axis";
	var yAxisName = "Y Axis";
	var userColor = "#ff0000";
	var nodeColor = "#999999";
	var latestData;

    var resizeTimeout;
	
	var e;
	var graph;
	
	
	var margin = {top: 20, right: 20, bottom: 70, left: 70};
	var width = 960;
	var height = 500;
	
	return {
        restrict: "E",
        link: function (scope, element, attrs) {

            e = element[0];

            var w = angular.element($window);

            scope.$watch('data', function (newVal, oldVal) {
                reloadData(scope);
            });

            w.bind('resize', function () {
                resizeStartTimeout(w, scope);
            });
            resize(w, scope);
        }
    };

	function resizeStartTimeout(w,scope) {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {resize(w,scope)},100);
	}

    function resize(w,scope) {
        width = w.width() - margin.left - margin.right;
	    height = w.height() - margin.top - margin.bottom;
	    reloadData(scope);
    }
	
	function reloadData(scope) {
		var data = scope.data;
		d3.select("svg").remove();
		graph = d3.select(e).append("svg")
				.attr("width", '100%')
				.attr("height", height + margin.top + margin.bottom)
			.append("g")
				.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		d3.select("svg").append("svg:defs").append("marker")
            .attr("id", "EndMarker")
            .attr("viewBox", "0 0 30 30")
            .attr("refX", 0)
            .attr("refY", 5)
            .attr("markerWidth", "30")
            .attr("markerHeight", "30")
            .attr("orient", "auto")
            .append("svg:path")
            .style("fill", function(d) { return d3.rgb(userColor); })
	        .attr("d", "M0,0 L10,5 L0,10");
	    d3.select("defs").append("marker")
            .attr("id", "StartMarker")
            .attr("viewBox", "0 0 30 30")
            .attr("refX", 0)
            .attr("refY", 5)
            .attr("markerWidth", "30")
            .attr("markerHeight", "30")
            .attr("orient", "auto")
            .append("svg:path")
            .style("fill", function(d) { return d3.rgb(userColor); })
	        .attr("d", "M10,0 L0,5 L10,10");
		// CAN BE DONE EARLIER
		// setup x 
		var xValue = function(d) { return d.x;}, // data -> value
		    xScale = d3.scale.linear().range([0, width]), // value -> display
		    xMap = function(d) { return xScale(xValue(d));}, // data -> display
		    xAxis = d3.svg.axis().scale(xScale).orient("bottom");
		
		// setup y
		var yValue = function(d) { return d.y;}, // data -> value
		    yScale = d3.scale.linear().range([height, 0]), // value -> display
		    yMap = function(d) { return yScale(yValue(d));}, // data -> display
		    yAxis = d3.svg.axis().scale(yScale).orient("left");
		    
		var cValue = function(d) { if(d.user == 'true') { addLines(d); return d3.rgb(userColor); } return d3.rgb(nodeColor); };
	
		// don't want dots overlapping axis, so add in buffer to data domain
        var theminx = d3.min(data, xValue);
        var theminy = d3.min(data, xValue);
        var themaxx = d3.max(data, xValue);
        var themaxy = d3.max(data, yValue);
        if(scope.min_x_value) { theminx = scope.min_x_value }
        if(scope.min_y_value) { theminy = scope.min_y_value }
        if(scope.max_x_value) { themaxx = scope.max_x_value }
        if(scope.max_y_value) { themaxy = scope.max_y_value }
        //themaxy += themaxy/10;
		xScale.domain([theminx, themaxx]);
		yScale.domain([theminy, themaxy]);

		// x-axis
		graph.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis)
		.append("text")
			.attr("class", "label")
			.attr("x", width/2)
			.attr("y", 48)
			.style("text-anchor", "middle")
			.text(scope.x_axis_label);

		// y-axis
		graph.append("g")
			.attr("class", "y axis")
			.call(yAxis)
		.append("text")
			.attr("class", "label")
			.attr("transform", "rotate(-90)")
			.attr("y", -28)
			.attr("x",height/-2)
			.attr("dy", "-1.2em")
			.style("text-anchor", "middle")
			.text(scope.y_axis_label);
			
		// draw dots
		graph.selectAll(".dot")
			.data(data)
		.enter().append("circle")
			.attr("class", "dot")
			.attr("r", 3)
			.attr("cx", xMap)
			.attr("cy", yMap)
			.style("fill", function(d) { return cValue(d);});

        function addLines(d) { 
            if(scope.showlines == 'true') {
            	var maxWidth = width + margin.left + margin.right - 80;
                var maxHeight = height + margin.top + margin.bottom;
                var showXArrow = false;
                var showYArrow = false;
                if(xMap(d) > maxWidth) {
                	showXArrow = true;
                }
                if(yMap(d) < -20) {
                	showYArrow = true;
                }
                if(showXArrow && showYArrow) {
	                graph.append("g").append('circle')
	                .attr("class", "dot")
					.attr("r", 10)
					.attr("cx", maxWidth+10)
					.attr("cy", -20)
					.style("fill", function(d) { return d3.rgb(userColor); })
                }
                //x axis line
                graph.append("g").append('svg:line')
                    .attr("x1", -100)
                    .attr("y1", yMap(d))
                    .attr("x2", maxWidth)
                    .attr("y2", yMap(d))
                    .attr("marker-end", function (d) {
                    	if(showXArrow) {
	                        return "url(#EndMarker)";
	                    }
	                    return "";
                    })
                    .style("stroke", d3.rgb(userColor));
                //y axis line
                graph.append("g").append('svg:line')
                    .attr("x1", xMap(d))
                    .attr("y1", -20)
                    .attr("x2", xMap(d))
                    .attr("y2", maxHeight)
                    .attr("marker-start", function (d) {
                    	if(showYArrow) {
	                        return "url(#StartMarker)";
	                    }
	                    return "";
                    })
                    .style("stroke", d3.rgb(userColor));
            }
        }
	}
	
});