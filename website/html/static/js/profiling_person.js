function display_personal_tags(){
	var oopts = {textHeight: 25,maxSpeed: 0.03,decel: 0.98,depth: 10.2,outlineColour: '#f6f',outlineThickness: 3,pulsateTo: 0.2,pulsateTime: 0.5,wheelZoom: false,textColour:'#00f',shadow:'#ccf',minBrightness:0.2,shadowBlur:3,weight:true,weightMode:'both'};
	redraw_tagcanvas();
	function redraw_tagcanvas() {
		if(!$('#myCanvas').tagcanvas(oopts,'tags_div')) {
			$('#myCanvas').hide();
		}
	}
}

function backToTop(){
	//当滚动条的位置处于距顶部100像素以下时，跳转链接出现，否则消失
	$(function () {
		$(window).scroll(function(){
			if ($(window).scrollTop()>100){
				$("#back-to-top").fadeIn(1500);
			}
			else
			{
				$("#back-to-top").fadeOut(1500);
			}
		});

		//当点击跳转链接后，回到页面顶部位置

		$("#back-to-top").click(function(){
			$('body,html').animate({scrollTop:0},1000);
			return false;
		});
	});
}

function display_layout(){
	$('#content').BlocksIt({
		numOfCol: 5,
		offsetX: 2,
		offsetY: 2
	});
}
//除法函数，用来得到精确的除法结果
//说明：javascript的除法结果会有误差，在两个浮点数相除的时候会比较明显。这个函数返回较为精确的除法结果。
//调用：accDiv(arg1,arg2)
//返回值：arg1除以arg2的精确结果
function accDiv(arg1,arg2){
    var t1=0,t2=0,r1,r2;
    try{t1=arg1.toString().split(".")[1].length}catch(e){}
    try{t2=arg2.toString().split(".")[1].length}catch(e){}
    with(Math){
        r1=Number(arg1.toString().replace(".",""))
        r2=Number(arg2.toString().replace(".",""))
        return (r1/r2)*pow(10,t2-t1);
    }
}

//给Number类型增加一个div方法，调用起来更加方便。
Number.prototype.div = function (arg){
    return accDiv(this, arg);
}

//乘法函数，用来得到精确的乘法结果
//说明：javascript的乘法结果会有误差，在两个浮点数相乘的时候会比较明显。这个函数返回较为精确的乘法结果。
//调用：accMul(arg1,arg2)
//返回值：arg1乘以arg2的精确结果
function accMul(arg1,arg2)
{
    var m=0,s1=arg1.toString(),s2=arg2.toString();
    try{m+=s1.split(".")[1].length}catch(e){}
    try{m+=s2.split(".")[1].length}catch(e){}
    return Number(s1.replace(".",""))*Number(s2.replace(".",""))/Math.pow(10,m)
}

//给Number类型增加一个mul方法，调用起来更加方便。
Number.prototype.mul = function (arg){
    return accMul(arg, this);
}

//加法函数，用来得到精确的加法结果
//说明：javascript的加法结果会有误差，在两个浮点数相加的时候会比较明显。这个函数返回较为精确的加法结果。
//调用：accAdd(arg1,arg2)
//返回值：arg1加上arg2的精确结果
function accAdd(arg1,arg2){
    var r1,r2,m;
    try{r1=arg1.toString().split(".")[1].length}catch(e){r1=0}
    try{r2=arg2.toString().split(".")[1].length}catch(e){r2=0}
    m=Math.pow(10,Math.max(r1,r2))
    return (arg1*m+arg2*m)/m
}

//给Number类型增加一个add方法，调用起来更加方便。
Number.prototype.add = function (arg){
    return accAdd(arg,this);
}

function display_community(){
	var width_1 = 700,
		height_1 = 394
	
	var svg_1 = d3.select("#community").append("svg")
		.attr("width", width_1)
		.attr("height", height_1);
	
	var force = d3.layout.force()
		.gravity(.05)
		.linkDistance([10,10,10,10,100,100,100,100,100,100,100,100,100,100,100])
		.distance(50)
		.charge(-420)
		.size([width_1, height_1]);
	
	d3.json("/profile/result.json?module=graph", function(json) {
	  force
		  .nodes(json.nodes)
		  .links(json.links)
		  .start();
	
	  var link = svg_1.selectAll(".link")
		  .data(json.links)
		.enter().append("line")
		  //.attr("class", "link")
		  .style("stroke", function(d) {return "#C00"; })
		  .style("stroke-width", function(d) {return (5).mul((d.value).div(10));});
	
	  var node = svg_1.selectAll(".node")
		  .data(json.nodes)
		.enter().append("g")
		  .attr("class", "node")
		  .call(force.drag);
	
	  node.append("image")
		  .attr("xlink:href", function(d) { return "/static/images/friends_profile_image/" + d.profile_image_url + '.jpg'})
		  .attr("x", function(d){
							  if(d.group == 0){return -20;}
							  else if(d.group == 5){return -8;}
							  else {return -16};
							  })
		  .attr("y", function(d){
							  if(d.group == 0){return -20;}
							  else if(d.group == 5){return -8;}
							  else {return -16};
							  })
		  .attr("width", function(d){
							  if(d.group == 0){return 40;}
							  else if(d.group == 5){return 16;}
							  else {return 32};
							  })
		  .attr("height", function(d){
							  if(d.group == 0){return 40;}
							  else if(d.group == 5){return 16;}
							  else {return 32};
							  })
		  .attr("class", "profile_image");
	
	  node.append("text")
		  .attr("dx", 16)
		  .attr("dy", 0)
		  .style("font-size", function(d) { 
								  if(d.group == 3){return 14 ;}
								  else if(d.group == 0){return 16;}
								   else if(d.group == 1){return 14;}
								    else if(d.group == 2){return 14;}
									 else if(d.group == 4){return 14;}
									 else if(d.group == 5){return 12;}
								  else{ return 14; }})
		  .text(function(d) { return d.name })
		  .style("stroke", function(d) { 
								  if(d.group == 3){return "#219EE2" ;}
								  else if(d.group == 0){return "#C90000";}
								   else if(d.group == 1){return "#3C9";}
								    else if(d.group == 2){return "rgb(193, 213, 47)";}
									 else if(d.group == 4){return "rgb(24, 0, 204)";}
									 else if(d.group == 5){return "black";}
								  else{ return "#C90000"; }});
	  node.append("text")
	  	.attr("dx", 16)
		.attr("dy", 18)
		.style("font-size", 12)
	  	.text(function(d) { return d.domain });
	
	  force.on("tick", function() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	
		node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	  });
	});
}

function display_d3_cloud(){
  var fill = d3.scale.category20();

  d3.layout.cloud().size([800, 300])
      .words([{text: "林彪", size: 11.2877123795*5}, {text: "腾冲", size: 11.2865568361*5}, {text: "中国远征军", size: 11.2865568361*5}, {text: "黄仁宇", size: 5.3279077918*5}, {text: "毛革", size: 9.78771145474*5}, {text: "九一三事件 ", size: 9.78771145474*5}, {text: "理想主义", size: 9.78771145474*5}, {text: "高华", size: 9.78771145474*5}, {text: "天下", size: 6.65730331428*5}, {text: "文革", size: 6.6302150609*5}, {text: "改革开放", size: 6.02094444185*5}, {text: "教授", size: 5.93892991855*5}, {text: "豆腐渣", size: 5.88402573053*5}, {text: "刘仰", size: 5.9259598521*5}, {text: "耳光", size: 5.93384872697*5}, {text: "政治" , size: 5.74903112281*5}, {text: "颜玉宏", size: 5.6126369809*5}, {text: "康复中心", size: 5.55077191779*5}, {text: "饥荒", size: 5.54695327391*5}, {text: "知识", size: 5.54695327391*5},{text: "共产党", size: 5.6336898333*5}, {text: "湿地", size: 5.62722896337*5}, {text: "#钓鱼岛#", size: 8*5}, {text: "#韩德强打人#", size: 8*5}, {text: "#一代宗师#", size: 7*5}, {text: "#马云辞任阿里CEO#", size: 5.4354545*5}, {text: "#质问广西＂有关单位＂#", size: 9*5}])
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


function friends_followers_analysis(){
	var chart = d3.parsets()
		  .dimensions(["FriendsOrFollowers", "Sex", "Age", "Group"]);
	
	var vis = d3.select("#vis_friends_followers").append("svg")
		.attr("width", 970)//chart.width())
		.attr("height", 622)//chart.height());
	
	d3.csv("/static/js/titanic.csv", function(csv) {
	    vis.datum(csv).call(chart);
	});
}

function display_filter_layout(){
      // This filter is later used as the selector for which grid items to show.
      var filter = '';
      var handler;
      
      // Prepare layout options.
      var options = {
        autoResize: true, // This will auto-update the layout when the browser window is resized.
        container: $('#content'), // Optional, used for some extra CSS styling
        offset: 2, // Optional, the distance between grid items
        itemWidth: 400 // Optional, the width of a grid item
      };
      
      // This function filters the grid when a change is made.
      var refresh = function() {
        // Clear our previous handler.
        if(handler) {
          handler.wookmarkClear();
          handler = null;
        }
        
        // This hides all grid items ("inactive" is a CSS class that sets opacity to 0).
        $('#content div.block').addClass('inactive');
        
        // Create a new layout selector with our filter.
        handler = $(filter);
        
        // This shows the items we want visible.
        handler.removeClass("inactive");
        
        // This updates the layout.
		console.log(filter);
		if(handler.attr('id') == '#tag_cloud_div'){
			handler.wookmark(setOptions('#content', 400));
		}
		else{
	        handler.wookmark(options);
		}
      }
	  
	  function setOptions(container_div, itemWidthOption){
		  return {
			  autoResize: true, // This will auto-update the layout when the browser window is resized.
			  container: $(container_div), // Optional, used for some extra CSS styling
			  offset: 4, // Optional, the distance between grid items
			  itemWidth: itemWidthOption // Optional, the width of a grid item
		  }
	  }
      
      /**
       * This function checks all filter options to see which ones are active.
       * If they have changed, it also calls a refresh (see above).
       */
      var updateFilters = function() {
        var oldFilter = filter;
        filter = '';
        var filters = [];
        
        // Collect filter list.
		var lis = $('#filters li');
        var i=0, length=lis.length, li;
        for(; i<length; i++) {
          li = $(lis[i]);
          if(li.hasClass('active')) {
            filters.push('#content div.block.'+li.attr('data-filter'));
          }
        }
        
        // If no filters active, set default to show all.
        if(filters.length == 0) {
          filters.push('#content div.block');
        }
        
        // Finalize our filter selector for jQuery.
        filter = filters.join(', ');
        
        // If the filter has changed, update the layout.
        if(oldFilter != filter) {
          refresh();
        }
      };
      
      /**
       * When a filter is clicked, toggle it's active state and refresh.
       */
      var onClickFilter = function(event) {
        var item = $(event.currentTarget);
        item.toggleClass('active');
        updateFilters();
      }
      
      // Capture filter click events.
      $('#filters li').click(onClickFilter);
      
      // Do initial update (shows all items).
      updateFilters();
}

$(document).ready(function(){
	
    display_personal_tags();
	display_community();
	display_d3_cloud();
	friends_followers_analysis();
	
	//display_filter_layout();
	backToTop();
	display_layout();
});
