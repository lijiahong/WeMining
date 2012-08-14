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
		    $('#information').text('在新浪微博关注此搜索框内的话题.');
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
	$('#information').text('在新浪微博关注此搜索框内的话题.');
	var _topic = $("#search_box")[0].value;
	if(_topic == " " || _topic == ''){
	    error('search_box', 3);
	    return;
	}
	else{
	    $.ajax({
		url: '/topicweibo/followtrends?topic='+_topic,
		dataType: 'json',
		success: function(d) {
		    if(d.status == 'is followed')
			$('#information').text('该话题您已经关注过了.');
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
    $.ajax({
	url: '/api/topic/now.json',
	dataType: 'json',
	success: function(d) {
	    for(type in d ){
		data = d[type];
		for(var i=0;i<data.length;i+=1){
                    data[i][0] = data[i][0].replace(/\s/g,"");
		    $('#hotTopics_'+type).append("<li><a href='#' class='tag" + data[i][2] + "' title='选择话题' onclick=autofulfill('" + data[i][0] + "')>" + data[i][0] + "</a></li>" );}
	    };
	}
    });
});
