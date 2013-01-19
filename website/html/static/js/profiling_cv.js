function display_personal_tags(){
	var oopts = {textHeight: 25,maxSpeed: 0.03,decel: 0.98,depth: 10.2,outlineColour: '#f6f',outlineThickness: 3,pulsateTo: 0.2,pulsateTime: 0.5,wheelZoom: false,textColour:'#00f',shadow:'#ccf',minBrightness:0.2,shadowBlur:3,weight:true,weightMode:'both'};
	redraw_tagcanvas();
	function redraw_tagcanvas() {
		if(!$('#myCanvas').tagcanvas(oopts,'tags_div')) {
			$('#myCanvas').hide();
		}
	}
}

function display_content_type_chart(){
	var pie_chart;
	
	var chartData = [
		{type:"URL", value:0.2},
		{type:"图片", value:0.25},
		{type:"视频", value:0.3},
		{type:"音频", value:0.25},
	];
	createPieChart();
	function createPieChart(){
		// PIE CHART
		pie_chart = new AmCharts.AmPieChart();
		pie_chart.dataProvider = chartData;
		pie_chart.titleField = "type";
		pie_chart.valueField = "value";
		pie_chart.outlineColor = "#FFFFFF";
		pie_chart.outlineAlpha = 0.8;
		pie_chart.outlineThickness = 2;
		// this makes the chart 3D
		pie_chart.depth3D = 15;
		pie_chart.angle = 30;
	
		// WRITE
		pie_chart.write("content_type_chart");
	}
}

function display_recent_topics(){
	var diameter = 800,
		format = d3.format(",d"),
		color = d3.scale.category20c();
	
	var bubble = d3.layout.pack()
		.sort(null)
		.size([diameter, diameter])
		.padding(1.5);
	
	var svg = d3.select("#recent_topic").append("svg")
		.attr("width", diameter)
		.attr("height", diameter)
		.attr("class", "bubble");
	
	d3.json("/profile/result.json?module=bubble", function(error, root) {
	  var node = svg.selectAll(".node")
		  .data(bubble.nodes(classes(root))
		  .filter(function(d) { return !d.children; }))
		.enter().append("g")
		  .attr("class", "node")
		  .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	
	  node.append("title")
		  .text(function(d) { return d.className + ": " + format(d.value); });
	
	  node.append("circle")
		  .attr("r", function(d) { return d.r; })
		  .style("fill", function(d) { return color(d.packageName); });
	
	  node.append("text")
		  .attr("dy", ".3em")
		  .style("text-anchor", "middle")
		  .text(function(d) { return d.className.substring(0, d.r / 3); });
	});
	
	// Returns a flattened hierarchy containing all leaf nodes under the root.
	function classes(root) {
	  var classes = [];
	
	  function recurse(name, node) {
		if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
		else classes.push({packageName: name, className: node.name, value: node.size});
	  }
	
	  recurse(null, root);
	  return {children: classes};
	}
	
	d3.select(self.frameElement).style("height", diameter + "px");
}


function display_community(){
	var width_1 = 800,
		height_1 = 500
	
	var svg_1 = d3.select("#community").append("svg")
		.attr("width", width_1)
		.attr("height", height_1);
	
	var force = d3.layout.force()
		.gravity(.05)
		.distance(200)
		.charge(-120)
		.size([width_1, height_1]);
	
	d3.json("/profile/result.json?module=graph", function(json) {
	  force
		  .nodes(json.nodes)
		  .links(json.links)
		  .start();
	
	  var link = svg_1.selectAll(".link")
		  .data(json.links)
		.enter().append("line")
		  .attr("class", "link");
	
	  var node = svg_1.selectAll(".node")
		  .data(json.nodes)
		.enter().append("g")
		  .attr("class", "node")
		  .call(force.drag);
	
	  node.append("image")
		  .attr("xlink:href", function(d) { return "/static/images/friends_profile_image/" + d.profile_image_url + '.jpg'})
		  .attr("x", -8)
		  .attr("y", -8)
		  .attr("width", 16)
		  .attr("height", 16)
		  .attr("class", "profile_image");
	
	  node.append("text")
		  .attr("dx", 12)
		  .attr("dy", ".35em")
		  .text(function(d) { return d.name });
	
	  force.on("tick", function() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	
		node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	  });
	});

}

function display_hashtags_vis(){
	/*if (document.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#BasicStructure", "1.1"))
    { */
	var tagColor = "#1D1D1B";
        function newpostReq(url,callBack)
        {
            var xmlhttp;
            if (window.XDomainRequest)
            {
                xmlhttp=new XDomainRequest();
                xmlhttp.onload = function(){callBack(xmlhttp.responseText)};
            }
            else if (window.XMLHttpRequest)
                xmlhttp=new XMLHttpRequest();
            else
                xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
            xmlhttp.onreadystatechange=function()
            {
                if (xmlhttp.readyState==4 && xmlhttp.status==200)
                    callBack(xmlhttp.responseText);
            }
            xmlhttp.open("GET",url,true);
            xmlhttp.send();
        }
    
		if (parent.frames.length > 0) 
            tagColor = "#74B77E";
			
        // Set width and height
        var w = 500;
        var h = 420;
        if ($("#logoVizContainer").size() > 0)
        {
            var wTemp = 800;
            //var wTemp = $(window).width();
			
            if (wTemp < 800)
                wTemp = 800;
            var hTemp = wTemp;
            $("#OKfestContainer").css({"top": -25});//-(wTemp - $("#logoVizContainer").height() - 50)/2});
            
        }
         else
        {
            var wTemp = $(window).width()-130;
            var hTemp = $(window).height()-100;
        }
        if(wTemp<=w || hTemp<=h) {}
        else if(wTemp>hTemp) {
        	h = hTemp;
        	w = hTemp+50;
        }
        else {
        	w = wTemp;
        	h = wTemp-50;
        }
        var r = w/2-130,
            maxLine = 2*r,
            minLine = 10,
            colors = ['#ff6666', '#66ccff', '#ffcc66'],
            nodes = [],
            links = [],
            //loose = [],
            maxTweetLength,
            minTweetLength,
            angleTwist = Math.random() * Math.PI;
            colorIndex = Math.round(Math.random() * colors.length);
        
        var logoTextWidth = w/8;
        var logoTextTop = h/2-logoTextWidth/3;
        var logoTextLeft = w/2-logoTextWidth/2;
        
        var vis = d3.select("#OKfestContainer").append("svg:svg")
                .attr("width", w)
                .attr("height", h);
        
        var force = d3.layout.force()
                .nodes(nodes)
                .links(links)
                .gravity(0.7)
                .linkDistance(function (link, index) { return linkLength(link.target.text.length); })
                .linkStrength(function (link, index) { return 0.1; })
                .charge(function (d) { if (d.type == "tag") return 0; if (d.type == 'linked') return -150000*r*r / (d3.select('#LogoVizNodes').selectAll("span")[0].length*450*450);})
                .size([w, h]);
        /*
        var looseForce = d3.layout.force()
                .nodes(loose)
                .gravity(0.8)
                .charge(-50)
                .size([w, h]);
        */
         function tick() {
            vis.selectAll("line.link")
              .attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });
        
            vis.selectAll("circle")
              .attr('cx', function (d) { return d.x})
              .attr('cy', function (d) { return d.y})
        }
        
        force.on("tick", tick);
        //looseForce.on("tick", loosetick)
        
        /*
        function loosetick() {
            vis.selectAll("circle.loose")
              .attr('cx', function (d) { return d.x})
              .attr('cy', function (d) { return d.y})
        }
        */
        function nextInLine()
        {
            var color = colors[colorIndex];
            colorIndex++;
            if (colorIndex >= colors.length)
                colorIndex = 0;
            return color;
        }
        
        function linkLength(length)
        {
            return ((maxLine - minLine)/(maxTweetLength - minTweetLength)) * (length - maxTweetLength) + maxLine;
        }
        
        function findItemIndex(id, array)
        {
            for (key in array)
            {
                if (array[key].id == id)
                    return key;
            }
            return false;
        }
        
        function formatTweet(tweet)
        {
            console.log(tweet);
            return '<p><strong>' + tweet.user + ':</strong> ' + tweet.text + '</p><p><a href="https://twitter.com/'+tweet.user+'/status/'+tweet.id+'" target="_blank">View in Twitter</a></p>';
        }
        
        function getRelatedTweets(tag)
        {
            var relatedTweets = [];
            vis.selectAll("line.link").each(function (d) {if (d.source.id == tag.id) {relatedTweets.push(d.target);};});
            var text = "<h1>"+tag.text+"</h1>";
            for (key in relatedTweets)
                text += "<div>"+ formatTweet(relatedTweets[key]) +"</div>";
            return text;
        }
        
        function calculateX(currentX, length, angle)
        {
            return  currentX + Math.cos(angle) * length;
        }
        
        function calculateY(currentY, length, angle)
        {
            return  currentY + Math.sin(angle) * length;
        }
        
        function updateData(starting) {
            newpostReq("/profile/result.json?module=hashtags_vis", function(json) {//http://floapps.com/lab/misc/oklogo/interface.json
                json = JSON.parse(json);
                minTweetLength = json.minLength;
                maxTweetLength = json.maxLength;
                
                var tagCount = 0;
                /*
                //updating loose nodes based on the loose array
                
                var ownLoose = d3.select('#LogoVizLoose').selectAll("span").data(json.loose, function (d) {return d.id});
                ownLoose.enter().append("span").each(function (d) { loose.push(d); });
                ownLoose.exit().each(function (d) {
                    var key = findItemIndex(d.id, loose);
                    if (key)
                    {
                        loose.splice(key, 1)
                    }
                }).remove();
        
        
                var loosenode = vis.selectAll("circle.loose").data(loose, function (d) {return d.id;});
        
                loosenode.enter().append("svg:circle")
                    .attr("cx", function (d) { return d.x })
                    .attr("cy", function (d) { return d.y })
                    .attr("class", "loose")
                    .attr("r", 2).on('click', function (d) {alert("hoi");});;
        
                loosenode.exit().remove()
        
        
                looseForce.start();
                */
                // we make spans to keep track of changing collections and updating links and nodes arrays
                var ownNodes = d3.select('#LogoVizNodes').selectAll("span").data(json.nodes, function (d) {return d.id});
                ownNodes.enter().append("span").each(function (d) { nodes.push(d); });
                ownNodes.each(function (d) {
                    if (d.type == "tag") {
                        tagCount++;
                        var key = findItemIndex(d.id, nodes);
                        if (key)
                        {
                            nodes[key].x = calculateX(w/2, r, d.angle + angleTwist);
                            nodes[key].y = calculateY(h/2, r, d.angle + angleTwist);
                        }
                    }
                }).on('click', function (d) {alert("hoi");});
        
                ownNodes.exit().each(function (d) {
                    var key = findItemIndex(d.id, nodes);
                    if (key)
                    {
                        nodes.splice(key, 1)
                    }
                }).remove();
                
                $("#tagCount").html(tagCount);
        
                var ownLinks = d3.select('#LogoVizLinks').selectAll("span").data(json.links, function (d) {return d.id});
                ownLinks.enter().append("span").each(function (d) { links.push({"target" : nodes[findItemIndex(d.targetid, nodes)], "source" : nodes[findItemIndex(d.sourceid, nodes)], id : d.id}); });
                ownLinks.exit().each(function (d) {
                    var key = findItemIndex(d.id, links);
                    if (key)
                    {
                        links.splice(key, 1)
                    }
                }).remove();
                //updating nodes based on the nodes array
                var node = vis.selectAll("circle.node").data(nodes, function (d) {return d.id;});
        
                node.enter().append("svg:circle")
                    .attr("cx", function (d) { if (d.type == "tag") return calculateX(w/2, r, d.angle + angleTwist); return d.x })
                    .attr("cy", function (d) { if (d.type == "tag") return calculateY(h/2, r, d.angle + angleTwist); d.y })
                    .attr("style", function (d) { if (d.type == "tag") return "fill:black;"; if (d.type == "tag" || d.type == "linked") return "display:none;" })
                    .attr("class", function (d) { if (d.type == "tag") return "node tag"; return "node"; })
                    .attr("r", 0.5)
                    .each(function (d) { if (d.type == "tag") d.color = nextInLine(); });
        
                node.exit().remove();
        
        
                //updating links based on the links array
                var link = vis.selectAll("line.link").data(links, function (d) {return d.id});
                link.enter().insert("svg:line")
                    .attr("class", "link")
                    .attr("x1", function(d) { return d.source.x; })
                    .attr("y1", function(d) { return d.source.y; })
                    .attr("x2", function(d) { return d.target.x; })
                    .attr("y2", function(d) { return d.target.y; })
                    .attr("style", function (d) { if (typeof d.source == "object") return "stroke:"+d.source.color; return "stroke:"+nodes[d.source].color;});
        
                link.exit().remove();
        
        
                //moving tags on the circle
                vis.selectAll("circle.tag").transition().each(function (d) {d.cx = d.x; d.px = d.x; d.cy = d.y; d.py = d.y;});
        
                var text = vis.selectAll("text.text").data(json.texts, function (d) {return d.id});
                text.enter().append("text")
                  .attr("x", function (d) {return calculateX(w/2, r, d.angle + angleTwist) + (Math.abs(Math.cos(d.angle + angleTwist)) < 0.2 ? - d.text.length * 4 : Math.cos(d.angle + angleTwist) > 0 ? 2 : - d.text.length * 8);})
                  .attr("y", function (d) {return calculateY(h/2, r, d.angle + angleTwist) + (Math.sin(d.angle + angleTwist) > 0 ? Math.sin(d.angle + angleTwist)*15 : -2);})
                  .attr("class", 'text')
				  .style("fill", tagColor)
                  .text(function(d) {return d.text;});
        
                vis.selectAll("line.link").on('click', function (d) {
					
                	d3.select('#LogoVizText #textNode').html(formatTweet(d.target));
					d3.select('#LogoVizText').style("left", d3.event.pageX-200+"px").style("top", d3.event.pageY-2200+"px").style("display", "block");//style("top", d3.event.pageY+20+"px")
                });
                d3.select('#closeTweet').on('click', function() {
        			d3.select('#LogoVizText').style("display", "none");
                });
                
                /*
                loosenode.on("click", function(d) {
                   d3.select('#LogoVizText').html(formatTweet(d));
                });
        
                */
                text
                    .on('click', function (d) {
                      /*  d3.select('#LogoVizText').html(getRelatedTweets(d)); */
                      window.open('http://twitter.com/#!/search/'+escape("#okfest "+d.text))
                    }).transition()
                  .attr("x", function (d) {return calculateX(w/2, r, d.angle + angleTwist) + (Math.abs(Math.cos(d.angle + angleTwist)) < 0.2 ? - d.text.length * 4 : Math.cos(d.angle + angleTwist) > 0 ? 2 : - d.text.length * 7);})
                  .attr("y", function (d) {return calculateY(h/2, r, d.angle + angleTwist) + (Math.sin(d.angle + angleTwist) > 0 ? Math.sin(d.angle + angleTwist)*15 : -2);});
        
                text.exit().remove();        
        
                force.start();
                /*
                if (starting === true)
                    for (var i = 0; i < 100; ++i) 
                    {
                        looseForce.tick();
                        force.tick();
                    }
                */
                
                if (json.minTime)
                {
                    $("#logoMinTime").html(json.minTime);
                    $("#logoMinMonth").html(json.minMonth);
                    $("#logoMinDay").html(json.minDay);
                    $("#infoBlock").show();
                }
            });
            
            //setTimeout(updateData, 60000);//每隔60s更新一次数据
        }
        // Logo text
    	$('#logoText').width(logoTextWidth);
    	$('#logoText').css({ 'top': logoTextTop, 'left': logoTextLeft });
    	$('#OKfestContainer').css({ "fontFamily": "Gudea, Sans Serif", 'width': r*2+260, 'height': h }).show();
        
        updateData(true);
    /*}
	
    else
    {
        $("#OKfestContainer").append("Your browser does not support the logo");
    } */
}

function display_community_pie(){
	var radius = 74,
		padding = 10;
	
	var color = d3.scale.ordinal()
		.range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
	
	var arc = d3.svg.arc()
		.outerRadius(radius)
		.innerRadius(radius - 30);
	
	var pie = d3.layout.pie()
		.sort(null)
		.value(function(d) { return d.population; });
	
	d3.csv("/static/js/community_pie.csv", function(error, data) {
	  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "State"; }));
	
	  data.forEach(function(d) {
		d.ages = color.domain().map(function(name) {
		  return {name: name, population: +d[name]};
		});
	  });
	
	  var legend = d3.select("#community_pie").append("svg")
		  .attr("class", "legend")
		  .attr("width", radius * 2)
		  .attr("height", radius * 2)
		.selectAll("g")
		  .data(color.domain().slice().reverse())
		.enter().append("g")
		  .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });
	
	  legend.append("rect")
		  .attr("width", 18)
		  .attr("height", 18)
		  .style("fill", color);
	
	  legend.append("text")
		  .attr("x", 24)
		  .attr("y", 9)
		  .attr("dy", ".35em")
		  .text(function(d) { return d; });
	
	  var svg = d3.select("#community_pie").selectAll(".pie")
		  .data(data)
		.enter().append("svg")
		  .attr("class", "pie")
		  .attr("width", radius * 2)
		  .attr("height", radius * 2)
		.append("g")
		  .attr("transform", "translate(" + radius + "," + radius + ")");
	
	  svg.selectAll(".arc")
		  .data(function(d) { return pie(d.ages); })
		.enter().append("path")
		  .attr("class", "arc")
		  .attr("d", arc)
		  .style("fill", function(d) { return color(d.data.name); })
		  .append("text")
		  .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
		  .attr("dy", ".35em")
		  .style("fill", "#FFF")
		  .style("text-anchor", "middle")
		  .text(function(d) { return d.data.population; });
	  /*
	  svg.selectAll(".arc").append("svg:text")
		  .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
		  .attr("dy", ".35em")
		  .style("text-anchor", "middle")
		  .text(function(d) { return d.data.population; });
	*/
	  svg.append("text")
		  .attr("dy", ".35em")
		  .style("text-anchor", "middle")
		  .text(function(d) { return d.State; });
	
	});
}

function display_d3_cloud(){
  var fill = d3.scale.category20();

  d3.layout.cloud().size([800, 300])
      .words([{text: "林彪", size: 11.2877123795*10}, {text: "腾冲", size: 11.2865568361*10}, {text: "中国远征军", size: 11.2865568361*10}, {text: "黄仁宇", size: 10.3279077918*10}, {text: "毛革", size: 9.78771145474*10}, {text: "九一三事件 ", size: 9.78771145474*10}, {text: "理想主义", size: 9.78771145474*10}, {text: "高华", size: 9.78771145474*10}, {text: "天下", size: 6.65730331428*10}, {text: "文革", size: 6.6302150609*10}, {text: "改革开放", size: 6.02094444185*10}, {text: "教授", size: 5.93892991855*10}, {text: "豆腐渣", size: 5.88402573053*10}, {text: "刘仰", size: 5.9259598521*10}, {text: "耳光", size: 5.93384872697*10}, {text: "政治" , size: 5.74903112281*10}, {text: "颜玉宏", size: 5.6126369809*10}, {text: "康复中心", size: 5.55077191779*10}, {text: "饥荒", size: 5.54695327391*10}, {text: "知识", size: 5.54695327391*10},{text: "共产党", size: 5.6336898333*10}, {text: "湿地", size: 5.62722896337*10}])
	  /*[
        "林彪", "world", "normally", "you", "want", "more", "words",
        "than", "this"].map(function(d) {
        return {text: d, size: 10 + Math.random() * 90};
      }))*/
      .rotate(function() { return ~~(Math.random() * 2) * 90; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw)
      .start();

  function draw(words) {
    d3.select("#d3_cloud").append("svg")
        .attr("width", 800)
        .attr("height", 300)
      .append("g")
        .attr("transform", "translate(400,150)")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
  }
}

$(document).ready(function(){
	display_personal_tags();
	display_recent_topics();
	display_content_type_chart();
	display_community();
	display_hashtags_vis();
	display_community_pie();
	display_d3_cloud();
});