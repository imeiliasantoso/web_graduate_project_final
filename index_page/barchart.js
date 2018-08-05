
   var margin_barchart = {top: 50, right:150, bottom: 10, left: 150},
        width_barchart = 1000 - margin_barchart.left - margin_barchart.right,
        height_barchart = 2500 - margin_barchart.top - margin_barchart.bottom;

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, height_barchart], .3);

    var x = d3.scale.linear()
        .rangeRound([0, width_barchart]);

    var color_barchart = d3.scale.ordinal()
        .range(["#c7001e", "#f6a580", "#fff"]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("top");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")

    var barchart = d3.select("#bar-figure").append("svg")
        .attr("width", width_barchart + margin_barchart.left + margin_barchart.right)
        .attr("height", height_barchart + margin_barchart.top + margin_barchart.bottom)
        .attr("id", "d3-plot")
      .append("g")
        .attr("transform", "translate(" + margin_barchart.left + "," + margin_barchart.top + ")");

      color_barchart.domain(["Subcribe", "Not Subcribe", ""]);

      d3.csv("index_page/data_attribute.csv", function(error, data) {

      data.forEach(function(e) {
        // calc percentages
        e["Subcribe"] = +e[1]*100/e.N;
        e["Not Subcribe"] = +e[2]*100/e.N;
        e[""] = +e[3]*100/e.N;
        var x0 = (e["Subcribe"]+e["Not Subcribe"]+e[""]);
       // var x0 = (e["Not Subcribe"]);


        var idx = 0;
        e.boxes = color_barchart.domain().map(function(name) { 
          return {
            name: name,
            x0: x0,
            x1: x0 += +e[name],
            N: +e.N,
            n: +e[idx += 1]}; });
      });

      var min_val = d3.min(data, function(e) {
              return e.boxes["0"].x0;
              });

      var max_val = d3.max(data, function(e) {
              return e.boxes["2"].x1;
              });

      x.domain([min_val, max_val]).nice();
      y.domain(data.map(function(e) { return e.Attribute; }));

      barchart.append("g")
          .attr("class", "x axis")
         //.call(xAxis);

      barchart.append("g")
          .attr("class", "y axis")
          .call(yAxis)

      var vakken = barchart.selectAll(".attribute")
          .data(data)
        .enter().append("g")
          .attr("class", "bar")
          .attr("transform", function(e) { return "translate(0," + y(e.Attribute) + ")"; });

      var bars = vakken.selectAll("rect")
          .data(function(e) { return e.boxes; })
        .enter().append("g").attr("class", "subbar");

      bars.append("rect")
          .attr("height", y.rangeBand())
          .attr("x", function(e) { return x(e.x0); })
          // .attr("width", function(e) { return x(e.x1) - x(e.x0); })
          .attr("width", function(e) { return x(e.x1) - x(e.x0); })
          .style("fill", function(e) { return color_barchart(e.name); });

      bars.append("text") 
          .attr("x", function(e) { return x(e.x0); })
          .attr("y", y.rangeBand()/2)
          .attr("dy", "0.5em")
          .attr("dx", "0.5em")
          .style("font" ,"10px sans-serif")
          .style("text-anchor", "begin")
          .style("fill", "#fff")
          .text(function(e) { return e.n !== 0 && (e.x1-e.x0)>3 ? e.n : "" });

      vakken.insert("rect",":first-child")
          .attr("height", y.rangeBand()*2)
          .attr("x", "1")
          .attr("width", width_barchart)
          .attr("fill-opacity", "0.5")
          .style("fill", "#0000")
         .attr("class", function(e,index) { return index%2==0 ? "even" : "uneven"; });


      barchart.append("g")
          .attr("class", "y axis")
      .append("line")
          .attr("x1", x(0))
          .attr("x2", x(0))
          .attr("y2", height_barchart);

      var startp = barchart.append("g").attr("class", "legendbox").attr("id", "mylegendbox");
      // this is not nice, we should calculate the bounding box and use that
      var legend_tabs = [0, 500, 1000, 1500, 2000];
      var legend_barchart = startp.selectAll(".legend")
          .data(color_barchart.domain().slice())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(e, i) { return "translate(" + legend_tabs[i] + ",-45)"; });

      legend_barchart .append("rect")
          .attr("x", 0)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color_barchart);

      legend_barchart .append("text")
          .attr("x", 22)
          .attr("y", 9)
          .attr("dy", "10px")
          .style("text-anchor", "begin")
          .style("font" ,"10px sans-serif")
          .text(function(e) { return e; });

      d3.selectAll(".axis path")
          .style("fill", "none")
          .style("stroke", "#000")
          .style("shape-rendering", "crispEdges")

      d3.selectAll(".axis line")
          .style("fill", "none")
          .style("stroke", "#000")
          .style("shape-rendering", "crispEdges")

      var movesize = width_barchart/2 - startp.node().getBBox().width_barchart/2;
      d3.selectAll(".legendbox").attr("transform", "translate(" + movesize  + ",0)");


    });
