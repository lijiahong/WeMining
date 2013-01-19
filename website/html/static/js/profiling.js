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

function display_thumbnail(){
	var options = {
			numOfCol: 5,
			offsetX: 8,
			offsetY: 8
	};
	
	//blocksit define
	$(window).load( function() {
		$('#thumbnail').BlocksIt(options);
	});
	
	//window resize
	var currentWidth = 1100;
	$(window).resize(function() {
		var winWidth = $(window).width();
		var conWidth;
		if(winWidth < 660) {
			conWidth = 440;
			col = 2
		} else if(winWidth < 880) {
			conWidth = 660;
			col = 3
		} else if(winWidth < 1100) {
			conWidth = 880;
			col = 4;
		} else {
			conWidth = 1100;
			col = 5;
		}
		
		if(conWidth != currentWidth) {
			currentWidth = conWidth;
			$('#thumbnail').width(conWidth);
			$('#thumbnail').BlocksIt({
				numOfCol: col,
				offsetX: 8,
				offsetY: 8
			});
		}
	});
	
	// Capture scroll event.
    $(document).bind('scroll', onScroll);
      
    // Load first data from the API.
    loadData();
	
	var handler = null;
    var page = 1;
    var isLoading = false;
    var apiURL = 'http://www.wookmark.com/api/json/popular';
	
	/**
     * When scrolled all the way to the bottom, add more tiles.
     */
    function onScroll(event) {
      // Only check when we're not still waiting for data.
      if(!isLoading) {
        // Check if we're within 100 pixels of the bottom edge of the broser window.
        var closeToBottom = ($(window).scrollTop() + $(window).height() > $(document).height() - 100);
        if(closeToBottom) {
          loadData();
        }
      }
    };
	
	/**
     * Refreshes the layout.
     */
    function applyLayout() {
      // Clear our previous layout handler.
      //if(handler) handler.wookmarkClear();
      
      // Create a new layout handler.
	  
      handler = $('#thumbnail');
      handler.BlocksIt(options);
    };
	
	/**
     * Loads data from the API.
     */
    function loadData() {
      isLoading = true;
      $('#loaderCircle').show();
      
      $.ajax({
        url: apiURL,
        dataType: 'jsonp',
        data: {page: page}, // Page parameter to make sure we load new data
        success: onLoadData
      });
    };
    
    /**
     * Receives data from the API, creates HTML for images and updates the layout
     */
    function onLoadData(data) {
      isLoading = false;
      $('#loaderCircle').hide();
      
      // Increment page index for future calls.
      page++;
      
      // Create HTML for the images.
      var html = '';
      var i=0, length=data.length, image;
      for(; i<length; i++) {
        image = data[i];
		
		html += '<div class="grid"><div class="imgholder">';
		html += '<img src="' + image.preview + '" /></div>';
		html += '<strong>' + i + '</strong>';
		html += '<p>' + image.title + '</p>';
		html += '<div class="meta">http://weibo.com</div>' + '</div>';
      }
      
      // Add image HTML to the page.
      $('#thumbnail').append(html);
      
      // Apply layout.
      applyLayout();
	}
}

$(document).ready(function(){
	display_thumbnail();
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
	var keywords = $("#search_box")[0].value;
	if(keywords == " " || keywords == ''){
	    error('search_box', 3);
	    return;
	}
	else{
	    window.location.href="/profile/cv";
	}
    });
    
    $("#follow_pic").click(function() {
	$('#information').text('将此搜索框内的名人加入关注列表.');
	var keywords = $("#search_box")[0].value;
	if(keywords == " " || keywords == ''){
	    error('search_box', 3);
	    return;
	}
	else{
	    $.ajax({
		url: '/topicweibo/followtrends?topic='+encodeURIComponent(keywords),
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
	
});
