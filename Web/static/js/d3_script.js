(function(){
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 980 - margin.left - margin.right,
        height = 676 - margin.top - margin.bottom;

    //Multiple line with differents color
    //var dataset = {{ data|safe }}

    var dataset =   [
        {
            'id': 1,
            'name': 'First Well',
            'coordinates':
                        [
                            {'x':1,'y':6, 'z': 0},{'x':2,'y':5, 'z': 1},{'x':3,'y':18, 'z': 3},{'x':4,'y':10, 'z': 4},
                            {'x':5,'y':2, 'z': 5},{'x':6,'y':24, 'z': 6},{'x':7,'y':13, 'z': 7},{'x':8,'y':4, 'z': 8}
                        ]
        },
        {
            'id': 2,
            'name': 'Second Well',
            'coordinates':
                        [
                            {'x':1,'y':7, 'z': 2},{'x':2,'y':5, 'z': 3},{'x':3,'y':9, 'z': 4},{'x':4,'y':5, 'z': 5},
                            {'x':5,'y':1, 'z': 6},{'x':6,'y':11, 'z': 7},{'x':7,'y':8, 'z': 8},{'x':8,'y':6, 'z': 9}
                        ]
        },
        {
            'id': 3,
            'name': 'Third Well',
            'coordinates':
                        [
                            {'x':1,'y':2, 'z': 3},{'x':2,'y':3, 'z': 4},{'x':3,'y':1, 'z': 5},{'x':4,'y':3, 'z': 6},
                            {'x':5,'y':0, 'z': 7},{'x':6,'y':5, 'z': 8},{'x':7,'y':3, 'z': 9},{'x':8,'y':3, 'z': 10}
                        ]
        },
        {
            'id': 4,
            'name': 'Fourth Well',
            'coordinates':
                        [
                            {'x':1,'y':2, 'z': 1},{'x':2,'y':0, 'z': 2},{'x':3,'y':2, 'z': 3},{'x':4,'y':2, 'z': 4},
                            {'x':5,'y':1, 'z': 5},{'x':6,'y':2, 'z': 6},{'x':7,'y':5, 'z': 7},{'x':8,'y':1, 'z': 8}
                        ]
        },
        {
            'id': 5,
            'name': 'Fifth Well',
            'coordinates':
                        [
                            {'x':1,'y':0, 'z': 5},{'x':2,'y':0, 'z': 6},{'x':3,'y':0, 'z': 7},{'x':4,'y':0, 'z': 8},
                            {'x':5,'y':1, 'z': 9},{'x':6,'y':1, 'z': 10},{'x':7,'y':0, 'z': 11},{'x':8,'y':2, 'z': 12}
                        ]
        }
    ];
    console.log(dataset);

    var color_scale = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]

    // append the SVG object to the body of the page
    var newSvg = d3.select("#multi")
                .append("svg")
                  .attr("width", width + margin.left + margin.right)
                  .attr("height", height + margin.top + margin.bottom)
                  .attr('viewBox', `0 0 ${(width + margin.left + margin.right)} ${height + margin.top + margin.bottom}`)
                  .attr('preserveAspectRatio', 'xMidYMid meet')
                .append("g")
                  .attr("transform",
                        "translate(" + margin.left + "," + margin.top + ")");

    // Add X axis
    var nx = d3.scaleLinear()
              .domain([0, 25])
              .range([0, width])

    var nxAxis = newSvg.append("g")
                   .attr('transform', 'translate(0,'+ height +')')
                   .call(d3.axisBottom(nx).tickSize(-height)) //

    // add Y axis
    var ny = d3.scaleLinear()
              .domain([0, 25])
              .range([height, 0])

    var nyAxis = newSvg.append('g')
                   .call(d3.axisLeft(ny).tickSize(-width)) //

    // Legend
    // for label for x axis and y axis
    newSvg.append("text").text("Y Label")
        .attr("x", -height / 2)
        .attr("y", -margin.left)
        .attr("dy","1em")
        .style("text-anchor", "middle")
        .attr("transform","rotate(-90)");

    newSvg.append("text").text("X Label")
        .attr("x", width / 2 )
        .attr("y", height+margin.bottom)
        .style("text-anchor", "middle");

    var nclip = newSvg.append('defs')
                      .append('svg:clipPath')
                      .attr('id', 'clip')
                      .append('svg:rect')
                      .attr('width', width)
                      .attr('height', height)
                      .attr('x', 0)
                      .attr('y', 0);

    var nscatter = newSvg.append('g')
                     .attr('clip-path', 'url(#clip)')

    // curveLinear, curveCardinal
    var nline = d3.line()
                 .curve(d3.curveLinear)
                 .x(d => nx(d.x))
                 .y(d => ny(d.y))

    //function(d, i) {return colors[i % colors.length]; }
    nscatter.selectAll('.line')
            .data(dataset)
            .enter()
            .append('path')
              .datum(function(d){return d.coordinates})
              .attr('class', 'line')
              .attr('fill', 'none')
              .attr('stroke', function(_, i){return color_scale[i % color_scale.length];})
              .attr('stroke-width', 1.5)
              .attr('d', nline)

    nscatter.selectAll('text')
            .data(dataset)
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
                .scaleExtent([0.5, 20])
                .extent([[0, 0], [width, height]])
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

    // Element
    d3.select('.first')
    .append('ul')
    .selectAll('li')
    .data(dataset)
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
        d3.select('.second').select('table').remove()
        var table = d3.select('.second').append('table')
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

    //File system solution
    d3.select('.btn-click-upload')
      .on('click', function(){
          d = T()
          d3.select('.buttons')
            .append('div')
            .attr('class', 'folder_list')
            .text(">>> " + d)
      });

    // Time getting when clicked
    function T() {
        var d = new Date();

        var yy = d.getFullYear();
        var mt = d.getMonth() + 1;
        var dd = d.getDate();
        var hh = d.getHours();
        var mm = d.getMinutes();
        var ss = d.getSeconds();

        // Verify and add a zero in front of numbers

        hh = checkTime(hh);
        mm = checkTime(mm);
        ss = checkTime(ss);
        mt = checkTime(mt);
        dd = checkTime(dd);

        var data = dd + "-" + mt + "-" + yy + "|" + hh + ":" + mm + ":" + ss;

        return data;
    }

    function checkTime(i) {
        if (i < 10){
            i = "0" + i;
        }
        return i;
    }
})();