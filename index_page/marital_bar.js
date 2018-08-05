
var margin = {top: 20, right: 30, bottom: 30, left: 60},
    width_marital = 360 - margin.left - margin.right,
    height_marital = 500 - margin.top - margin.bottom;

var x0_marital = d3.scale.ordinal()
    .rangeRoundBands([0, width_marital], .1);

var x1_marital = d3.scale.ordinal();

var y1_marital = d3.scale.linear()
    .range([height_marital, 0]);

var xAxis_marital = d3.svg.axis()
    .scale(x0_marital)
    .tickSize(0)
    .orient("bottom");

var yAxis_marital = d3.svg.axis()
    .scale(y1_marital)
    .orient("left");

var color = d3.scale.ordinal()
    .range(["#ca0020","#f4a582","#d5d5d5","#92c5de","#0571b0"]);

var chart2 = d3.select('#chart2').append("svg")
    .attr("width", width_marital + margin.left + margin.right)
    .attr("height", height_marital + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json("index_page/marital_data.json", function(error, data) {

  var categoriesNames = data.map(function(d) { return d.categorie; });
  var rateNames = data[0].values.map(function(d) { return d.rate; });

  x0_marital.domain(categoriesNames);
  x1_marital.domain(rateNames).rangeRoundBands([0, x0_marital.rangeBand()]);
  y1_marital.domain([0, d3.max(data, function(categorie) { return d3.max(categorie.values, function(d) { return d.value; }); })]);


  chart2.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height_marital + ")")
      .call(xAxis_marital);

  chart2.append("g")
      .attr("class", "y axis")
      .style('opacity','0')
      .call(yAxis_marital)
  .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 2)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .style('font-weight','bold')
      .text("Value");

  chart2.select('.y').transition().duration(500).delay(1300).style('opacity','1');

  var slice2 = chart2.selectAll(".slice")
      .data(data)
      .enter().append("g")
      .attr("class", "g")
      .attr("transform",function(d) { return "translate(" + x0_marital(d.categorie) + ",0)"; });

  slice2.selectAll("rect")
      .data(function(d) { return d.values; })
  .enter().append("rect")
      .attr("width", x1_marital.rangeBand())
      .attr("x", function(d) { return x1_marital(d.rate); })
      .style("fill", function(d) { return color(d.rate) })
      .attr("y", function(d) { return y1_marital(0); })
      .attr("height", function(d) { return height_marital - y1_marital(0); })
      .on("mouseover", function(d) {
          d3.select(this).style("fill", d3.rgb(color(d.rate)).darker(2));
      })
      .on("mouseout", function(d) {
          d3.select(this).style("fill", color(d.rate));
      });

  slice2.selectAll("rect")
      .transition()
      .delay(function (d) {return Math.random()*1000;})
      .duration(1000)
      .attr("y", function(d) { return y1_marital(d.value); })
      .attr("height", function(d) { return height_marital - y1_marital(d.value); });

  //Legend
  var legend_marital = chart2.selectAll(".legend")
      .data(data[0].values.map(function(d) { return d.rate; }).reverse())
  .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d,i) { return "translate(0," + i * 20 + ")"; })
      .style("opacity","0");

  legend_marital.append("rect")
      .attr("x", width_marital - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", function(d) { return color(d); });

  legend_marital.append("text")
      .attr("x", width_marital - 18)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) {return d; });

  legend_marital.transition().duration(500).delay(function(d,i){ return 1300 + 100 * i; }).style("opacity","1");

}); 
