function getUrlParam(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
    var r = window.location.search.substr(1).match(reg); 
    if (r != null){ 
	return decodeURI(r[2]); 
    }
    return null; 
}
// Date format
Date.prototype.format = function(format)
{ 
  var o = { 
    "M+" : this.getMonth()+1, //month 
    "d+" : this.getDate(),    //day 
    "h+" : this.getHours(),   //hour 
    "m+" : this.getMinutes(), //minute 
    "s+" : this.getSeconds(), //second 
    "q+" : Math.floor((this.getMonth()+3)/3),  //quarter 
    "S" : this.getMilliseconds() //millisecond 
  } 
  if(/(y+)/.test(format)) 
      format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
  for(var k in o)
      if(new RegExp("("+ k +")").test(format)) 
	  format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length)); 
  return format; 
} 

//Retweet animation
var paused = 1;
var step = 0;
var total_step = 20;
var node_sizes = {};
var timer = null;
var ranked_status = 0;

// Mouse position when dragging
var oldX = 0,
oldY = 0,
	
// Position of mousedown
clickedX = 0,
clickedY = 0,
	
// True if currently dragging map
dragging = false,
// True if map has been moved since last mousedown
mapMoved = false,

// True if currently dragging zoom bar
zoomBarDragging = false,
// Zoom bar knob's offset from the top of the zoom bar
offsetTop = 0,

// Zoom levels
zoomLevel = 0,
MIN_ZOOM_LEVEL = -1,
MAX_ZOOM_LEVEL = 6,

// Amount to zoom in by for each zoom level
ZOOM_FACTOR = 1.7,

// Map dimensions
MAP_WIDTH,
MAP_HEIGHT,

// Preload hand image
myPic = new Image(32, 32);
myPic.src = "/static/images/closedhand.ico";

// Used to perform SVG zooms to the current mouse location
var stateTf;

Event.observe(window, 'load', function() {
    topic = getUrlParam('q');
    console.log(topic);
    $('query_keywords').value = topic;
    // Display warning for browsers that don't support SVG
    if (!$("svg").preserveAspectRatio) {
	$("svg").style.visibility = "hidden";
	$("popup").innerHTML = "你的浏览器不支持SVG图像,去装个现代的浏览器吧!";
	$("popup").style.visibility = "visible";
	$("map").style.cursor = "default";
	$("popup").style.backgroundColor = "black";
	$("popup").style.top = "200px";
	$("popup").style.left = "180px";
	return;
    }
    
    MAP_WIDTH = $("map").getWidth();
    MAP_HEIGHT = $("map").getHeight();
    
    //Display warning for IE
    if (navigator.appName === "Microsoft Internet Explorer") {
	addCloseButtonToPopup();
	var p = document.createElement("p");
	p.textContent = "有些特性也许在IE浏览器上无法体验,建议使用谷歌、火狐等浏览器.";
	p.style.lineHeight = "1.7em";
	$("popup").appendChild(p);
	$("popup").style.width = "280px";
	centerPopup();
	$("popup").style.padding = "10px";
	$("popup").style.visibility = "visible";
    }

    Event.observe("svg", "mousedown", mouseDown);
    Event.observe("svg", 'dblclick', doubleClick);
    Event.observe(document, "mouseup", mouseUp);
    Event.observe(document, "mousemove", mouseMove);
    
    Event.observe("search", "submit", search);
    $("query").disabled = "";
    
    var outerCircles = document.getElementsByClassName("outer");
    innerCircles = document.getElementsByClassName("inner"),
    outerMouseUpFunction = function() { if (!mapMoved) { mouseClick(this); }},
    outerMouseOverFunction = function() { mouseOver(this); },
    outerMouseOutFunction = function() { mouseOut(this); },
    innerMouseUpFunction = function() { if (!mapMoved) { mouseClick(this.previousElementSibling); }},
    innerMouseOverFunction = function() { mouseOver(this.previousElementSibling); },
    innerMouseOutFunction = function() { mouseOut(this.previousElementSibling); };
    for (i = outerCircles.length - 1; i >= 0; i--) {
	// Use mouseup instead of onclick so clicking down on a node and dragging does not open the popup
	Event.observe(outerCircles[i], 'mouseup', outerMouseUpFunction);
	Event.observe(outerCircles[i], 'mouseover', outerMouseOverFunction);
	Event.observe(outerCircles[i], 'mouseout', outerMouseOutFunction);
	
	Event.observe(innerCircles[i], 'mouseup', innerMouseUpFunction);
	Event.observe(innerCircles[i], 'mouseover', innerMouseOverFunction);
	Event.observe(innerCircles[i], 'mouseout', innerMouseOutFunction);
    }

    zoomBarSetup();
    
    Event.observe($("play"), 'click', play_animation);
    Event.observe($("stop"), 'click', stop_animation);
    Event.observe($("submit"), 'click', click_analysis);
    Event.observe($("more_rank"), 'click', more_rank);
	
    // Handle the search default text
    Event.observe("query", "focus", function() { if (this.value  === "找人" ) { this.value = ""; } });
    Event.observe("query", "blur", function() { if (this.value === "") { this.value = "找人"; } });

    // Handle the search default text
    Event.observe("query_keywords", "focus", function() { if (this.value  === "请输入关键词" ) { this.value = ""; } });
    Event.observe("query_keywords", "blur", function() { if (this.value === "") { this.value = "请输入关键词"; } });
    
    // Mouse wheel setup
    if (navigator.userAgent.toLowerCase().indexOf('webkit') >= 0) {
	$("svg").addEventListener('mousewheel', mouseWheel, false); // Chrome/Safari
    }
    else {
	$("svg").addEventListener('DOMMouseScroll', mouseWheel, false); // Others
    }
    $('time').textContent = '';
    first_play_animation();
    
    
});

function zoomBarSetup() {
    var zoomBar, zoomBarPlus, zoomBarSlider, zoomBarSliderNotch, notchOnClick, zoomBarMinus, zoomBarKnob;
	
    zoomBar = document.createElement("div");
    zoomBar.id = "zoomBar";
    $("map").appendChild(zoomBar);
    
    zoomBarPlus = document.createElement("div");
    zoomBarPlus.id = "zoomBarPlus";
    zoomBarPlus.onclick = function() { zoomCenter(1); };
    zoomBar.appendChild(zoomBarPlus);
    
    zoomBarSlider = document.createElement("div");
    zoomBarSlider.id = "zoomBarSlider";
    zoomBar.appendChild(zoomBarSlider);
    // Create the notches on the zoom bar
    notchOnClick = function() { setZoomLevel(this.getAttribute("notch")); };
    for (i = MIN_ZOOM_LEVEL; i <= MAX_ZOOM_LEVEL; i++) {
	zoomBarSliderNotch = document.createElement("div");
	zoomBarSliderNotch.setAttribute("notch", i);
	$(zoomBarSliderNotch).addClassName("notch");
	zoomBarSliderNotch.style.position = "absolute";
	zoomBarSliderNotch.style.top = (MAX_ZOOM_LEVEL - i) * 10 + 5 + "px";
	zoomBarSliderNotch.onclick = notchOnClick;
	zoomBarSlider.appendChild(zoomBarSliderNotch);
    }
    
    zoomBarMinus = document.createElement("div");
    zoomBarMinus.id = "zoomBarMinus";
    zoomBarMinus.onclick = function() { zoomCenter(0); };
    zoomBar.appendChild(zoomBarMinus);
    
    zoomBarKnob = document.createElement("img");
    zoomBarKnob.src = "/static/images/zoomBarKnob.png";
    zoomBarKnob.id = "zoomBarKnob";
    zoomBarKnob.unselectable = "on";
    Event.observe(zoomBarKnob, 'mousedown', zoomBarKnobMouseDown);
    Event.observe(document, 'mouseup', zoomBarKnobMouseUp);
    Event.observe(document, 'mousemove', zoomBarKnobMouseMove);
    zoomBarSlider.appendChild(zoomBarKnob);
    zoomBarKnob.style.top = (MAX_ZOOM_LEVEL - zoomLevel) * 10 + 5 + "px";
}

//first play animation
function first_play_animation() {
    button = $('play');
    data = analysis_data();
    var groups = data.groups;
    var max_group_length = data.max_group_length;
    if(paused){
	paused = 0;
	reset_graph();
	button.textContent = '暂停';
	timer = new PeriodicalExecuter(draw_graph, 2);
    }
    else{
	paused = 1;
	button.textContent = '播放';	
    }
}

//show loading when clik analysis button
function click_analysis(event) {
    // console.log('analysis click');
    $('svg_region').hide();
    $('data').hide();
    stop_animation(null);
    $('loading').show();
    $('map').style.backgroundColor = "#C0C0C0";
    var p = document.createElement("p");
    p.textContent = "请稍候,数据加载中...";
    // p.setStyle({
    // 	lineHeight: "1.7em",
    // 	fontSize: "250%",
    // 	width: "280px",
    // 	padding: "10px",
    // 	visibility: "visible"
    // });
    p.style.lineHeight = "1.7em";
    p.style.fontSize = "200%";
    $("popup").appendChild(p);
    
    // $("popup").style.width = "280px";
    centerPopup();
    $("popup").style.padding = "10px";
    $("popup").style.visibility = "visible";
}

//play animation
function play_animation(event) {
    button = event.target;
    data = analysis_data();
    var groups = data.groups;
    var max_group_length = data.max_group_length;
    if(paused){
	paused = 0;
	reset_graph();
	button.textContent = '暂停';
	timer = new PeriodicalExecuter(draw_graph, 1);
    }
    else{
	paused = 1;
	button.textContent = '播放';
    }
}

//reset graph
function reset_graph() {
    $('time').textContent = '';
    $('count').textContent = '';
    innerCircles = document.getElementsByClassName("inner");
    for (i = innerCircles.length - 1; i >= 0; i--) {
	innerCircles[i].setAttributeNS(null, "fill", "white");
    }
    for(var node_id in node_sizes){
	size = node_sizes[node_id];
	$(node_id).setAttributeNS(null, "fill", "black");
	$(node_id).setAttributeNS(null, "rx", size);
	$(node_id).setAttributeNS(null, "ry", size);
    }
}

//stop animation
function stop_animation(event) {
    if(timer){
	timer.stop();
	step = 0
	paused = 1;
	reset_graph();
	$("play").textContent = '播放';
    }
}

//analysis data from inner circles, sepreate them into groups for animation
function analysis_data() {
    innerCircles = document.getElementsByClassName("inner");
    length = innerCircles.length;
    ts_array = []
    groups = [];
    for(var i=0;i<length;i++){
	data = innerCircles[i].previousElementSibling.previousElementSibling.textContent;
	ts = data.split('|')[1];
	if(!isNaN(ts))
	   ts_array.push(ts);
    }
    ts_array = unique_array(ts_array);
    ts_array.sort();
    ts_series = [];
    max_group_length = 0;

    // each_step = Math.floor(ts_array.length / total_step);
    // index = 0;
    // index += each_step;
    // while(index < ts_array.length){
    // 	ts_series.push(ts_array[index])
    // 	index += each_step;
    // }
    // if(!(index == ts_array.length-1))
    // 	ts_series.push(ts_array[ts_array.length-1]);

    var datehash = new Hash();
    for(var i=0;i<ts_array.length;i++){
    	ts = ts_array[i];
    	cdate = new Date(ts*1000).format("yyyy-MM-dd");
    	datehash.set(cdate, ts);
    }
    ts_series = datehash.values().sort();

    // groups.push(['0']);
    for(var i=0;i<ts_series.length;i++){
	p_end = i==0 ? 0 : ts_series[i-1];
	end = ts_series[i];
	group = [];
	for(var j=0;j<length;j++){
	    try{
		ts = $(''+j).previousElementSibling.textContent.split('|')[1];
		if(!isNaN(ts)){
		    if(ts <= end && ts > p_end){
			// if(j == 0){
			//     continue
			// }
			// if($(''+j).previousElementSibling.getAttribute("class") == 'key'){
			//     groups.push([''+j]);
			//     continue
			// }
			group.push(''+j);
		    }
		}
	    }catch(e){
		//console.log(j);
	    }
	}
	if(max_group_length < group.length)
	    max_group_length = group.length;
	groups.push(group);
    }
    return {'groups': groups,
	    'max_group_length': max_group_length
	   }
}

//get unique array
function unique_array(array) {
    tempArray=array.slice(0);
    for(var i=0;i<tempArray.length;i++){
	for(var j=i+1;j<tempArray.length;){
	    if(tempArray[j]==tempArray[i]){
		tempArray.splice(j,1);
	    }
	    else{
		j = j + 1;
	    }					  				 
	}
    }
    return tempArray;
}

//expand node_size
function expand_node(node_id) {
    //store current size
    node_sizes[node_id] = $(node_id).rx.baseVal.value;
    new_size = 1.5 * $(node_id).rx.baseVal.value;
    $(node_id).setAttributeNS(null, "rx", new_size);
    $(node_id).setAttributeNS(null, "ry", new_size);
    
}

//draw retweet count in period
function draw_count(power) {
    $('count').textContent = '转发数量: ' + power
}

//draw graph as time going on
function draw_graph() {
    if(!paused){
	if(step < groups.length){
	    group = groups[step];
	    power = group.length
	    draw_count(power);
	    try{
		ts_end = $(''+group[group.length-1]).previousElementSibling.textContent.split('|')[1];
		ts_start = $(''+group[0]).previousElementSibling.textContent.split('|')[1];
		end_date = new Date(ts_end*1000);
		start_date = new Date(ts_start*1000);
	    }catch(e){
		step += 1;
		return;
	    }
	    $('time').textContent = '时间: '+start_date.format("yyyy-MM-dd");
	    for(var i=0;i<group.length;i++){
		node_id = ''+group[i];
		if(node_id == '0') {
		    $(node_id).nextElementSibling.setAttributeNS(null, "fill", "yellow");
		    expand_node(node_id);
		    continue;
		}
		if($(node_id).previousElementSibling.getAttribute("class") == 'key') {
		    $(node_id).nextElementSibling.setAttributeNS(null, "fill", "blue");
		    expand_node(node_id);
		}
		else{
		    $(node_id).nextElementSibling.setAttributeNS(null, "fill", "red");
		}
	    }
	    step += 1;
	}
	else{
	    if(timer){
		timer.stop();
		step = 0
		paused = 1;
		innerCircles = document.getElementsByClassName("inner");
		$("play").textContent = '播放';
	    }
	}
    }
}

function more_rank(){
    sections = document.getElementsByClassName("section");
    for(var i=0;i<sections.length;i++){
	section = sections[i];
	count = 0;
	section.select('li').each(function(el){
	    if(count >= 5){
		if(!ranked_status){
		    $(el).show();
		}
		else{
		    $(el).hide();
		}
	    }
	    count += 1;
	});
    }
    ranked_status = !ranked_status;
    if(ranked_status)
	$('more_rank').textContent = '隐藏'
    else
	$('more_rank').textContent = '更多排名'
}


// Show the name of the retweet-user in a popup when hovering over the node
function mouseOver(node) {
    if ($("popup").nodeId === node.id) { return; }
    
    mouseOut(node);
    
    // Set inner circle's class to current
    node.nextElementSibling.className.baseVal = "inner current";
    
    var hoverPopup = document.createElement("p");
    hoverPopup.textContent = node.previousElementSibling.previousElementSibling.textContent;
    hoverPopup.id = "hoverPopup";
    hoverPopup.nodeId = node.id;
    
    // Add arrow to popup
    var arrow = document.createElement("div");
    arrow.addClassName("arrow");
    hoverPopup.appendChild(arrow);
    
    $("map").appendChild(hoverPopup);
    
    recalculateHoverPopupPosition();
    hoverPopup.style.visibility = "visible";
}

// Remove the hover popup onmouseout
function mouseOut(node) {
    if ($("hoverPopup")) {
	$("map").removeChild($("hoverPopup"));
    }
    // Remove "current" class from inner circle's class
    node.nextElementSibling.className.baseVal = "inner";
}

function recalculateHoverPopupPosition() {
    if (!$("hoverPopup")) { return; }
    
    // Do all the calculations necessary to make sure that the hover
    // popup is pointing to the correct node
    var hoverPopup = $("hoverPopup"),
    node = $(hoverPopup.nodeId),
    arrow = hoverPopup.childElements()[0],
    
    mapOffsetX = -$("viewport").getCTM().e,
    mapOffsetY = -$("viewport").getCTM().f,
    zoomScale = Math.pow(ZOOM_FACTOR, zoomLevel),
    nodeXPosition = node.cx.baseVal.value,
    nodeYPosition = node.cy.baseVal.value,
    nodeRadius = node.rx.baseVal.value;
    
    
    hoverPopup.style.padding = hoverPopup.style.left = hoverPopup.style.top = "0px";
    hoverPopup.style.width = "auto";
    hoverPopup.style.height = "auto";
    
    // For IE9, increase width by 1 to prevent new lines in hover popup
    // This is pretty much a hack
    if (navigator.appName === "Microsoft Internet Explorer") {
	hoverPopup.style.width = hoverPopup.getWidth() + 1 + "px";
    }
    // Set the hover popup's dimensions so it does not change when scrolled out of view
    // This is pretty much a hack too
    hoverPopup.style.width = hoverPopup.getWidth() + "px";
    hoverPopup.style.height = hoverPopup.getHeight() + "px";
    
    // Set padding in javascript to not affect the width
    // If we try to set the padding in CSS, getting the dimensions in Javascript becomes problematic
    hoverPopup.style.padding = "3px 5px";
    hoverPopup.style.left = nodeXPosition * zoomScale * 0.3 - mapOffsetX - hoverPopup.getWidth() / 2 + "px";
    hoverPopup.style.top = nodeYPosition * zoomScale * 0.3 - mapOffsetY - nodeRadius * zoomScale * 0.3 - 35 + "px";
    
    arrow.style.top = hoverPopup.getHeight() + "px";
    arrow.style.left = hoverPopup.getWidth() / 2 - arrow.getWidth() / 2 + "px";
}

function mouseDown(e) {
    if (e.preventDefault) {
	e.preventDefault();
    }
    e.returnValue = false;
	
    dragging = true;
    
    oldX = clickedX = e.clientX;
    oldY = clickedY = e.clientY;

    stateTf = $("viewport").getCTM().inverse();
	
    $("map").style.cursor = "url(/static/images/closedhand.ico), pointer";
}

function mouseUp(e) {
    if (e.preventDefault) {
	e.preventDefault();
    }
    e.returnValue = false;
    
    mapMoved = false;
    dragging = false;
    $("map").style.cursor = "url(/static/images/openhand.ico), pointer";
}

function mouseMove(e) {
    if (!dragging) { return; }
    mapMoved = true;
    
    var zoomScale = Math.pow(ZOOM_FACTOR, zoomLevel);
    
    // If popup is tied to a node, move it with the screen
    // The popup can exist without a nodeId if it is showing search results
    if ($("popup").nodeId) {
	$("popup").style.left = e.clientX - oldX + parseInt($("popup").style.left, 10) + "px";
	$("popup").style.top = e.clientY - oldY + parseInt($("popup").style.top, 10) + "px";
    }
    
    // Move the map accordingly
    setCTM($("viewport"), stateTf.inverse().translate((e.clientX - clickedX) / (zoomScale * 0.3), (e.clientY - clickedY) / (zoomScale * 0.3)));
    
    oldX = e.clientX;
    oldY = e.clientY;
}

function search(e) {
    if (e) { Event.stop(e); }
    if ($("query").value.length === 0) { return; }
    $("popup").style.visibility = "hidden";

    // Search svg text for building
    resetPopup();
    var user_names = document.getElementsByClassName("user_name")
    for (i = user_names.length - 1; i >= 0; i--) {
	if($("query").value == user_names[i].textContent){
	    user_id = user_names[i].nextElementSibling.nextElementSibling.id
	    snapToUser($(user_id));
	    return
	}   
    }
    // Add close button
    addCloseButtonToPopup();
    
    // No user found
    var p = document.createElement("p");
    p.textContent = "谁也没找到，换个名字试试吧!";
    p.style.lineHeight = "1.7em";
    $("popup").appendChild(p);
    
    $("popup").style.width = "280px";
    centerPopup();
    $("popup").style.padding = "10px";
    $("popup").style.visibility = "visible";

}

// Move the map to the clicked user
function snapToUser(node) {
    var transform = $("viewport").getCTM(),
    x = transform.e,
    y = transform.f,
    zoomScale = Math.pow(ZOOM_FACTOR, zoomLevel),
    
    nodeXPosition = node.cx.baseVal.valueAsString,
    nodeYPosition = node.cy.baseVal.valueAsString;
    
    setCTM($("viewport"), $("viewport").getCTM().translate((MAP_WIDTH / 2 - x) / (zoomScale * 0.3) - nodeXPosition, (MAP_HEIGHT / 2 - y) / (zoomScale * 0.3) - nodeYPosition));
    
    mouseClick(node);
}

/**
 * Handle clicking on a node.
 */
function mouseClick(node) {
    $("popup").style.visibility = "hidden";
    
    // True if we clicked the same node that is already attached to the popup
    // If it is true we will just hide the popup
    var sameNodeClicked = ($("popup").nodeId == node.id);
    
    resetPopup();
    
    if (sameNodeClicked) { return; }
    
    // Set the nodeId field to the current node's id
    $("popup").nodeId = node.id;
    
    // data[0] text
    // data[1] ts
    var data = node.previousElementSibling.textContent.split("|")
    // Add arrow to popup
    var arrow = document.createElement("div");
    arrow.addClassName("arrow");
    $("popup").appendChild(arrow);
    
    // Show user name
    // var user_name = document.createElement("strong");
    // user_name.textContent = node.previousElementSibling.previousElementSibling.textContent;
    // $("popup").appendChild(user_name);

    var user_href = document.createElement("a");
    user_href.textContent = node.previousElementSibling.previousElementSibling.textContent;
    user_href.href = 'http://idec.buaa.edu.cn:8080/search?q='+node.previousElementSibling.previousElementSibling.textContent;
    user_href.target = '_blank'
    $("popup").appendChild(user_href);
    
    // Add close button
    addCloseButtonToPopup();

    //Add user text
    var user_text = document.createElement("p");
    user_text.style.width = '300px'
    user_text.textContent = data[0];
    $("popup").appendChild(user_text);

    //Add user post time
    var user_post_time = document.createElement("p");
    ts = data[1]
    if(!isNaN(ts)){
	date = new Date(ts*1000);
	user_post_time.textContent = date.format("yyyy-MM-dd hh:mm:ss");}
    else{
	user_post_time.textContent = ts
    }
    $("popup").appendChild(user_post_time);


    recalculatePopupPosition();
    
    // Change the padding back to the default
    $("popup").style.padding = "10px";
    
    $("popup").style.visibility = "visible";

    mouseOut(node);
}


/******************************************************** Zoom functions **********************************************************/
// Handle zooming
// zoomIn (0 or 1) - zoom in 1, zoom out 0
// x - x mouse coordinate of zoom
// y - y mouse coordinate of zoom
function zoom(zoomIn, x, y) {
    // Debug
    //$("query").value = "x: " + x + ",y: " + y;
    
    // Return if invalid zoom
    if ((zoomIn && zoomLevel == MAX_ZOOM_LEVEL) || (!zoomIn && zoomLevel == MIN_ZOOM_LEVEL)) {
	return false;
    }
    
    // New scale matrix in current mouse position
    var k;
    
    // Zoom in
    if (zoomIn) {
	zoomLevel++;
	k = $("svg").createSVGMatrix().translate(x, y).scale(ZOOM_FACTOR).translate(-x, -y);
    }
    
    // Zoom out
    else {
	zoomLevel--;
	k = $("svg").createSVGMatrix().translate(x, y).scale(1 / ZOOM_FACTOR).translate(-x, -y);		
    }
    
    $("zoomBarKnob").style.top = (MAX_ZOOM_LEVEL - zoomLevel) * 10 + 5 + "px";

    setCTM($("viewport"), $("viewport").getCTM().multiply(k));

    if (typeof(stateTf) == "undefined") {
	stateTf = $("viewport").getCTM().inverse();
    }
    stateTf = stateTf.multiply(k.inverse());
    
    recalculatePopupPosition();
    recalculateHoverPopupPosition();
    
    return true;
}

function zoomBarKnobMouseDown(e) {
    //if (!e) { e = window.event; }
    //Event.extend(e);
    Event.stop(e);

    zoomBarDragging = true;
    offsetTop = parseInt($("zoomBarKnob").style.top, 10) - e.clientY;
    
    $("zoomBarKnob").style.cursor = "url(/static/images/closedhand.ico), pointer";
}

function zoomBarKnobMouseUp(e) {
    if (!zoomBarDragging) { return; }
    zoomBarDragging = false;
    $("zoomBarKnob").style.cursor = "url(/static/images/openhand.ico), pointer";
    
    var newZoomLevel = MAX_ZOOM_LEVEL - parseInt(parseInt($("zoomBarKnob").style.top, 10) / 10, 10);
    setZoomLevel(newZoomLevel);
}

function zoomBarKnobMouseMove(e) {
    //if (!e) { e = window.event; }
    //Event.extend(e);
    
    if (zoomBarDragging) {
	$("zoomBarKnob").style.top = e.clientY + offsetTop + "px";
	
	var topOfSlider = 5;
	if ($("zoomBarKnob").offsetTop < topOfSlider) { $("zoomBarKnob").style.top = topOfSlider + "px"; }
	var bottomOfSlider = (MAX_ZOOM_LEVEL - MIN_ZOOM_LEVEL) * 10 + 5;
	if ($("zoomBarKnob").offsetTop > bottomOfSlider) { $("zoomBarKnob").style.top = bottomOfSlider + "px"; }
    }
}

function setZoomLevel(newZoomLevel) {
    while (newZoomLevel < zoomLevel) { zoomCenter(0); }
    while (newZoomLevel > zoomLevel) { zoomCenter(1); }
}

/**
 * Zoom in on double click
 */
function doubleClick(evt) {
    var p = getEventPoint(evt);
    p = p.matrixTransform($("viewport").getCTM().inverse());
    
    zoom(1, p.x, p.y);
}

/**
 * Handle mouse wheel event.
 */
function mouseWheel(evt) {
    if (evt.preventDefault)
	evt.preventDefault();
    evt.returnValue = false;
    
    //								(Chrome/Safari)			(Mozilla)
    var delta = (evt.wheelDelta) ? evt.wheelDelta / 3600 : evt.detail / -90;
    
    var p = getEventPoint(evt);
    p = p.matrixTransform($("viewport").getCTM().inverse());
    
    zoom(Math.ceil(delta), p.x, p.y);
}

function zoomCenter(zoomIn) {
    var mapOffsetX = -$("viewport").getCTM().e,
    mapOffsetY = -$("viewport").getCTM().f,
    zoomScale = Math.pow(ZOOM_FACTOR, zoomLevel);
    
    zoom(zoomIn, (MAP_WIDTH / 2 + mapOffsetX) / (zoomScale * 0.3), (MAP_HEIGHT / 2 + mapOffsetY) / (zoomScale * 0.3));
}

function resetPopup() {
    var popup = $("popup");
    popup.nodeId = "";
    popup.style.padding = popup.style.left = popup.style.top = "0px";
    popup.style.width = "auto";
    popup.style.height = "auto";
    while (popup.childElements().length > 0) {
	popup.removeChild(popup.childElements()[0]);
    }
}

/************************************************************* Popup Helpers ****************************************************/

function centerPopup() {
    $("popup").style.top = MAP_HEIGHT / 2 - $("popup").offsetHeight / 2 + "px";
    $("popup").style.left = MAP_WIDTH / 2 - $("popup").offsetWidth / 2 + "px";
}

function recalculatePopupPosition() {
    if (!$("popup").nodeId) return;
    $("popup").style.padding = $("popup").style.left = $("popup").style.top = "0px";
    $("popup").style.width = "auto";
    $("popup").style.height = "auto";
    
    // Hack so the popup will not change dimensions when it gets scrolled out of view
    $("popup").style.width = $("popup").getWidth() + "px";
    $("popup").style.height = $("popup").getHeight() + "px";
    
    // Position the popup while we have node's position
    var node = $($("popup").nodeId),
    // mapOffsetX & mapOffsetY - how far the map has been scrolled in both
    // the x and y directions. Some number between 0 and MAX_DIMENSION * MAX_ZOOM_LEVEL
    mapOffsetX = -$("viewport").getCTM().e,
    mapOffsetY = -$("viewport").getCTM().f,
    zoomScale = Math.pow(ZOOM_FACTOR, zoomLevel),
    
    // nodeXPosition & nodeYPosition - position of the node in the map
    // Some number between 0 and 960 or 0 and 500
    nodeXPosition = node.cx.baseVal.value,
    nodeYPosition = node.cy.baseVal.value,
    nodeRadius = node.rx.baseVal.value;
    
    // Calculate the position of the popup
    // 0 < left < 960
    // 0 < top < 500
    $("popup").style.left = nodeXPosition * zoomScale * 0.3 - mapOffsetX - 10 + "px";
    $("popup").style.top = nodeYPosition * zoomScale * 0.3 - mapOffsetY - 20 + "px";
    
    arrow = $$("#popup .arrow")[0];
    
    if ($("popup").offsetLeft < 600) {
	arrow.removeClassName("arrowRight");
	arrow.addClassName("arrowLeft");
	arrow.style.left = "-10px";
    }
    else {
	arrow.removeClassName("arrowLeft");
	arrow.addClassName("arrowRight");
	arrow.style.left = $("popup").getWidth() + 20 + "px";
    }
    
    // Offset the left position depending on which side the popup should appear on
    if ($("popup").offsetLeft < 600) {
	// Show popup on right side of node
	$("popup").style.left = $("popup").offsetLeft + nodeRadius * zoomScale * 0.3 + 25 + "px";
    }
    else {
	// Show popup on left side of node
	$("popup").style.left = $("popup").offsetLeft - $("popup").getWidth() - nodeRadius * zoomScale * 0.3 - 25 + "px";
    }
    $("popup").style.padding = "10px";
}

function addCloseButtonToPopup() {
    var closeButton = document.createElement("span");
    closeButton.textContent = "x";
    closeButton.addClassName("close");
    closeButton.onclick = function() { $("popup").nodeId = null; $("popup").style.visibility = "hidden"; };
    $("popup").appendChild(closeButton);
}