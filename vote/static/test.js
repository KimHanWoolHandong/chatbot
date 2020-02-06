(function (d3$1) {
  'use strict';

  var width = 360, height = 700;
  const svg = d3.select('#map');
  const g = svg.append('g');

  var graphData = [50, 30, 12, 5, 3];
  var pieG = d3.pie();
  var arc = d3.arc().innerRadius(0).outerRadius(40);
  var pieElements = d3.select("#myGraph")
  	.selectAll("path")
  	.data(pieG(graphData));

  pieElements
  	.enter()
      .append("path")
        .attr("class", "pie")
        .attr("d", arc)
        .attr("transform", "translate(200, 50)")
        .style("fill", "white")
        .style("stroke", 'black');

}(d3));