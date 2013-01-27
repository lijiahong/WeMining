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
};

function checkClose(){
	var status = $("#openClose").attr("class");
	if(status == 'open'){
		$("#openClose").attr("class", "open opend");
		$("#shadow_nav").attr("class", "noclosed");
	}
	else{
		$("#openClose").attr("class", "open");
		$("#shadow_nav").attr("class", "closed");
		
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

$(document).ready(function(){
	display_thumbnail();
    backToTop();
});
