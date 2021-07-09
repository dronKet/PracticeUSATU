(function(){
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 980 - margin.left - margin.right,
        height = 776 - margin.top - margin.bottom;

    //Colors for graphs
    var color_scale = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]

    // SVG for graph creation
    var newSvg = d3.select("#multi")
                    .append("svg")
                      .attr("width", width + margin.left + margin.right)
                      .attr("height", height + margin.top + margin.bottom)
                      .attr('viewBox', `0 0 ${(width + margin.left + margin.right)} ${height + margin.top + margin.bottom}`)
                      .attr('preserveAspectRatio', 'xMidYMid meet')
                    .append("g")
                      .attr("transform",
                            "translate(" + margin.left + "," + margin.top + ")")
                    .on('mousemove', function(event) {
                        let coords = d3.mouse(this);
                        console.log( coords[0], coords[1] ) // log the mouse x,y position
                    });

    // Add X axis
    var nx = d3.scaleLinear()
              .domain([152000, 156000])
              .range([0, width])

    var nxAxis = newSvg.append("g")
                       .attr("transform", 'translate(0, ' + (height) + ')')
                       .call(d3.axisBottom().scale(nx).tickSize([-height]))
                       .selectAll('text')
                         .attr('transform', 'translate(0, -15)')


    // add Y axis
    var ny = d3.scaleLinear()
              .domain([136000, 143000])
              .range([height, 0])

    var nyAxis = newSvg.append('g')
                   .call(d3.axisLeft(ny).tickSize([-width]))
                   .selectAll('text')
                         .attr('transform', 'translate(43, 0)')



    // curveLinear, curveCardinal
    var nline = d3.line()
                  .curve(d3.curveLinear)
                  .x(d => nx(d.x))
                  .y(d => ny(d.y))

    //Graph by element
    d3.select('.buttons')
      .append('ul')
      .selectAll('li')
      .data(alldatas)
      .enter()
      .append('li')
      .text(d => d.name)
      .on('click', function(d) {
          var dataseT = d.files

          d3.select('.buttons').selectAll('li')
              .style('background-color','#5dc6ff24')
              .style('color', 'black')

          d3.select(this)
              .style('background-color', '#fff')
              .style('color', '#a7a7a7')

          newSvg.selectAll('defs').exit().remove()
          var a = document.querySelector('#scatter_lines')
          if (a !== null) {
            a.remove()
          }
          newSvg.select('g').select('rect').remove()

          var nscatter = newSvg.append('g')
                         .attr('id', 'scatter_lines')
                         .attr('clip-path', 'url(#clip)')

          var nclip = newSvg.append('defs')
                          .append('svg:clipPath')
                          .attr('id', 'clip')
                          .append('svg:rect')
                          .attr('width', width)
                          .attr('height', height)
                          .attr('x', 0)
                          .attr('y', 0);

          nscatter.selectAll('.line')
                      .data(dataseT)
                      .enter()
                      .append('path')
                        .datum(function(d){return d.coordinates})
                        .attr('class', 'line')
                        .attr('fill', 'none')
                        .attr('stroke', function(_, i){return color_scale[i % color_scale.length];})
                        .attr('stroke-width', 1.5)
                        .attr('d', nline)

          nscatter.selectAll('text')
                  .data(dataseT)
                  .enter()
                  .append('text')
                  .text(d => d.name)
                  .attr('class', 'path_text')
                  .attr('x', x => nx(+x.coordinates[x.coordinates.length - 1].x) + 1)
                  .attr('y', y => ny(+y.coordinates[y.coordinates.length - 1].y) + 1)
                  .attr('dy', ".35em")
                  .attr("font-family", "Arial, Helvetica, sans-serif")
                  .attr("fill", "Black")
                  .style("font", "normal 12px Arial")

          // zooming part
          var nzoom = d3.zoom()
                      .scaleExtent([0, 100])
                      .extent([[-width, -height], [width, height]])
                      .on('zoom', nzoomed)

          // Rectangle (invisible) adding on top of the chart area
          newSvg.append('rect')
              .attr('width', width)
              .attr('height', height)
              .style('fill', 'none')
              .style('pointer-events', 'all')
              .call(nzoom);

          function nzoomed() {
            // new scale
            var nnewX = d3.event.transform.rescaleX(nx)
            var nnewY = d3.event.transform.rescaleY(ny)

            nxAxis.call(d3.axisBottom(nnewX).tickSize(-height))
            nyAxis.call(d3.axisLeft(nnewY).tickSize(-width))

            //update line curveCardinal
            var newLine = d3.line()
                            .curve(d3.curveLinear)
                            .x(d => nnewX(d.x))
                            .y(d => nnewY(d.y))

            nxAxis.transition().duration(1000).call(d3.axisBottom(nnewX).tickSize(-height))
            nyAxis.transition().duration(1000).call(d3.axisLeft(nnewY).tickSize(-width))
            nscatter.selectAll('.line')
                    .attr('d', newLine)

            nscatter.selectAll('text')
                    .attr('x', x => nnewX(+x.coordinates[x.coordinates.length - 1].x) + 1)
                    .attr('y', y => nnewY(+y.coordinates[y.coordinates.length - 1].y) + 1)
          }
        d3.select('.first')
        .select('ul').remove()

        // Element
        d3.select('.first')
        .append('ul')
        .selectAll('li')
        .data(dataseT)
        .enter()
        .append('li')
        .text(d => d.name)
        .style('color', function(_, i){ return color_scale[i]; })
        .on('click', function(d, i){
            d3.select('.first').selectAll('li')
              .style('color', function(_, i){ return color_scale[i]; })
              .style('background-color', '#d8d8d8')

            d3.select(this)
              .style('color', '#a7a7a7')
              .style('background-color', '#fff')

            d3.select('.second')
            .selectAll('div')
            .remove()

            // Table
            tab(d.coordinates, ['x', 'y', 'z']);

            d3.selectAll('.line')
                .attr('stroke-width', 1.5)

            d3.select(this)
              .attr('id', i)

            d3.selectAll('.line').filter(":nth-child(" + (parseInt(this.id) + 1).toString() + ")")
              .attr('class', 'line ' + (parseInt(this.id) + 1).toString())
              .attr('stroke-width', 3.5)

            d3.selectAll(".path_text")
              .style('font-weight', 'normal')
              .style('font-size', '12px')

            d3.selectAll(".path_text").filter(function(d, k){
                return i === k ? true : false
            })
              .style("font-weight", "bold")
              .style("font-size", "16px")
        })

        // Function to create table
        function tab(data, columns) {
            d3.select('.second').select('div').select('table').remove()
            var table = d3.select('.second').append('div').append('table')
            var thead = table.append('thead')
            var	tbody = table.append('tbody');
            var tabe = ['X', 'Y', 'Z']

            // append the header row
            thead.append('tr')
                 .selectAll('th')
                 .data(tabe).enter()
                 .append('th')
                 .text(c => c);

            // create a row for each object in the data
            var rows = tbody.selectAll('tr')
                            .data(data)
                            .enter()
                            .append('tr');

            // create a cell in each row for each column
            var cells = rows.selectAll('td')
                            .data(function(row){
                                return columns.map(function(column){
                                    return {column: column, value: row[column]};
                                });
                            })
                            .enter()
                            .append('td')
                                .text(function (d) { return d.value; });

            return table
        }
      })
})();