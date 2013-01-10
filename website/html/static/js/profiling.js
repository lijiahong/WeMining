function autofulfill(word){
    document.getElementById("search_box").value = word;
}

function normal(id, times){
    var obj = $("#"+id);
    obj.css("background-color","#FFF");
    if(times < 0) {
        return;
    }
    times = times-1;
    setTimeout("error('"+id+"',"+times+")",150);
}

function error(id, times) {
    var obj = $("#"+id);
    obj.css("background-color","#F6CECE");
    times = times-1;
    setTimeout("normal('"+id+"',"+times+")",150);
}

$(document).ready(function(){
    $("#search_box").tagSuggest({
	url: '/api/topic/suggest.json',
	delay: 250
    });
    $('.bubbleInfo').each(function () {
	// options
	var distance = 10;
	var time = 250;
	var hideDelay = 500;

	var hideDelayTimer = null;

	// tracker
	var beingShown = false;
	var shown = false;
	
	var trigger = $('.trigger', this);
	var popup = $('.popup', this).css('opacity', 0);

	// set the mouseover and mouseout on both element
	$([trigger.get(0), popup.get(0)]).mouseover(function () {
	    // stops the hide event if we move from the trigger to the popup element
	    if (hideDelayTimer) clearTimeout(hideDelayTimer);

	    // don't trigger the animation again if we're being shown, or already visible
	    if (beingShown || shown) {
		return;
	    } else {
		beingShown = true;

		// reset position of popup box
		popup.css({
		    top: 35,
		    left: 600,
		    width:300,
		    display: 'block' // brings the popup back in to view
		})

		// (we're using chaining on the popup) now animate it's opacity and position
		    .animate({
			top: '-=' + distance + 'px',
			opacity: 1
		    }, time, 'swing', function() {
			// once the animation is complete, set the tracker variables
			beingShown = false;
			shown = true;
		    });
	    }
	}).mouseout(function () {
	    // reset the timer if we get fired again - avoids double animations
	    if (hideDelayTimer) clearTimeout(hideDelayTimer);
	    
	    // store the timer so that it can be cleared in the mouseover if required
	    hideDelayTimer = setTimeout(function () {
		hideDelayTimer = null;
		popup.animate({
		    top: '-=' + distance + 'px',
		    opacity: 0
		}, time, 'swing', function () {
		    // once the animate is complete, set the tracker variables
		    shown = false;
		    // hide the popup entirely after the effect (opacity alone doesn't do the job)
		    popup.css('display', 'none');
		    $('#information').text('将此搜索框内的名人加入关注列表.');
		});
	    }, hideDelay);
	});
    });
    $("#search_button").click(function() {
	var _topic = $("#search_box")[0].value;
	if(_topic == " " || _topic == ''){
	    error('search_box', 3);
	    return;
	}
	else{
	    window.location.href="/topicweibo/analysis?topic=" + _topic;
	}
    });
    
    $("#follow_pic").click(function() {
	$('#information').text('将此搜索框内的名人加入关注列表.');
	var _topic = $("#search_box")[0].value;
	if(_topic == " " || _topic == ''){
	    error('search_box', 3);
	    return;
	}
	else{
	    $.ajax({
		url: '/topicweibo/followtrends?topic='+encodeURIComponent(_topic),
		dataType: 'json',
		success: function(d) {
		    if(d.status == 'is followed')
			$('#information').text('该名人您已经加入关注列表.');
		    else if(d.status == 'follow ok')
			$('#information').text('关注成功.');
		    else if(d.status == 'need login')
			$('#information').text('请登录新浪微博.');
		    else
			$('#information').text('关注失败.');
		}
	    });	    
	}
    });
	
	var diameter = 960,
		format = d3.format(",d"),
		color = d3.scale.category20c();
	
	var bubble = d3.layout.pack()
		.sort(null)
		.size([diameter, diameter])
		.padding(1.5);
	
	var svg = d3.select("body").append("svg")
		.attr("width", diameter)
		.attr("height", diameter)
		.attr("class", "bubble");
	
	d3.json("/static/js/flare.json", function(error, root) {
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
});
