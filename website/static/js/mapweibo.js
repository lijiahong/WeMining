var oopts = {textHeight: 25,maxSpeed: 0.05,decel: 0.98,depth: 0.92,outlineColour: '#f6f',outlineThickness: 3,pulsateTo: 0.2,pulsateTime: 0.5,wheelZoom: false,textColour:'#00f',shadow:'#ccf',minBrightness:0.2,shadowBlur:3,weight:true,weightMode:'both'};
function redraw_tagcanvas() {
		if(!$('#myCanvas').tagcanvas(oopts,'tags_div')) {
			$('#myCanvas').hide();
		}
}	

var DOM = {
		splashScreen : (function () {
			var htmlElement = '<div id="splash-screen"><img src="/static/images/splash.png"></div>';
			var $element;
			var reposition = function () {
				this.find('img').css({
					left:  ($(window).width() - 530) / 2 + 'px',
					top:  ($(window).height() - 312) / 2 + 'px'     
				});
			};
			return {
				init : function () {
					$element = $('body').append(htmlElement).find('#splash-screen');
					$element.reposition = reposition;
					$(window).bind('resize', function () {
						$element.reposition();
					}).trigger('resize');
					$element.bind('click', function (){
						$(this).remove();
					});
				}
			};
		})(),
};

function change_nav(module){
	$("#nav").empty();
	if(module == 1){
		var nav_htmlElement = '<a href="javascript:change_nav(0);" style="width: 200px; left:0px; "id="nav-act"  >全网话题推荐</a><a href="javascript:void(0)"style="width: 400px; background: #5bb4e5; left:200px;" >新浪微博个人话题推荐</a> <div class="clear"></div>';
		getTopics(1);
	}
	if(module == 0){
		var nav_htmlElement = '<a href="javascript:void(0);" style="width: 400px; background: #5bb4e5; left: 0px;">新浪微博全网话题推荐</a><a href="javascript:change_nav(1)" style="width: 200px; left: 400px;" id="nav-act">个人话题推荐</a> <div class="clear"></div>';
		getTopics(0);
	}
	$("#nav").append(nav_htmlElement);
}

var select_top;



function getTopics(module){
	var request;
	if(module == 1){
		request = '/gettopics/personal';
	}
	if(module == 0){
		request = '/gettopics/all';
	}
	$.ajax({
				  url : request,
				  dataType : 'json',    
				  //contentType: "application/x-www-form-urlencoded; charset=utf-8", 
				  success : function (data) {
					  $("#tags_ul").empty();
					  $("#select_topic").empty();
					  
					  $("#select_topic_dammy").remove();
					  for (var i=0;i<data.length;i=i+2) {
						$("#tags_ul").append("<li><a href='#' style=\"font-size:"+data[i+1]+"ex\">"+data[i]+"</a></li>");
						if(i == 0){
							$("#select_topic").append("<option value='" + data[i] + "' selected='selected'>" + data[i] + "</option>");
						}
						else{
							$("#select_topic").append("<option value='" + data[i] + "'>" + data[i] + "</option>");
						}
					  };
					  getNumber($("#select_topic").val());
					  
					  
					  $("#select_topic").jQselectable({
							style: "simple",
							set: "fadeIn",
							out: "fadeOut",
							height: 150,
							opacity: .9,
							callback: function(){
								if($(this).val().length>0){ 
									  getNumber($(this).val());				 
								}
							}
					  });
						

					  redraw_tagcanvas();
				  },
	        });
}


function getNumber(topic){
		var seriesOptions = [],
        yAxisOptions = [],
        seriesCounter = 0,
        names = ['total'],
        colors = Highcharts.getOptions().colors;

    $.each(names, function(i, name) {
        $.getJSON('/getWeiboNum?topic=' + topic + '&filename=' + name,    function(data) {
		//$.getJSON('http://www.highcharts.com/samples/data/jsonp.php?filename='+ name.toLowerCase() +'-c.json&callback=?',    function(data) {
            seriesOptions[i] = {
                name: name,
                data: data,
                //pointInterval: 3600 * 1000,
            };

            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter++;

            if (seriesCounter == names.length) {
                createChart();
            }
        });
    });



    // create the chart when all data is loaded
    function createChart() {

        chart = new Highcharts.StockChart({
            chart: {
                renderTo: 'container',
				borderWidth: 1,
				width:970,
				//height: 200
            },

            rangeSelector: {
				buttons: [{
                    type: 'day',
                    count: 3,
                    text: '3d'
                }, {
                    type: 'week',
                    count: 1,
                    text: '1w'
                }, {
                    type: 'month',
                    count: 1,
                    text: '1m'
                }, {
                    type: 'month',
                    count: 6,
                    text: '6m'
                }, {
                    type: 'year',
                    count: 1,
                    text: '1y'
                }, {
                    type: 'all',
                    text: 'All'
                }],
                selected: 3
            },

            yAxis: {
				title: {
                    text: '微博数量'
                },
                /*labels: {
                    formatter: function() {
                        return this.value;
                    }
                },
                plotLines: [{
                    value: 0,
                    width: 3,
                    color: 'silver'
                }]*/
				
            },
			
			title: {
                text: '微博数量的时间分布曲线'
            },
    
            subtitle: {
                text: '话题：' +  $("#select_topic").val()  // dummy text to reserve space for dynamic subtitle
            },
            /*
            plotOptions: {
                series: {
                    compare: 'value'
                }
            },*/
            
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2
            },
            
            series: seriesOptions
        });
    }
	
	}


$(document).ready(function() {
		//DOM.splashScreen.init();
		change_nav(0);
		$('#starttime').jdPicker();
		$('#endtime').jdPicker();
		
		//console.log($('#starttime').val());
		//console.log($('#starttime').val());
		
		
		$("#select_timeInterval").jQselectable({
							style: "simple",
							set: "fadeIn",
							out: "fadeOut",
							height: 150,
							opacity: .9,
							callback: function(){
								if($(this).val().length>0){ 
									 		 
								}
							}
						});
						
						
		
		
		$("#nav-act").hover(function() {
        $(this).stop(true).animate({
            height:"36px"
        },300);
    	}, function() {
       		$(this).stop(true).animate({
            	height:"24px"
        	},300);
    	});
		redraw_tagcanvas();
		
		/*
		$.ajax({
				  url : '/gettopics',
				  dataType : 'json',    
				  //contentType: "application/x-www-form-urlencoded; charset=utf-8", 
				  success : function (data) {
					  $("#tags_ul").empty();
					  $("#select_topic").empty();
					  for (var i=0;i<data.length;i=i+2) {
						$("#tags_ul").append("<li><a href='#' style=\"font-size:"+data[i+1]+"ex\">"+data[i]+"</a></li>");
						if(i == 0){
							$("#select_topic").append("<option value='" + data[i] + "' selected='selected'>" + data[i] + "</option>");
						}
						else{
							$("#select_topic").append("<option value='" + data[i] + "'>" + data[i] + "</option>");
						}
					  };
					  getNumber($("#select_topic").val());
					  $("#select_topic").jQselectable({
							style: "simple",
							set: "fadeIn",
							out: "fadeOut",
							height: 150,
							opacity: .9,
							callback: function(){
								if($(this).val().length>0){ 
									  getNumber($(this).val());				 
								}
							}
						});
					  redraw_tagcanvas();
				  },
	        });
	 		*/
	
});
