Date.prototype.format = function(format){
    var o = {
	"M+" : this.getMonth()+1, //month
	"d+" : this.getDate(),    //day
	"h+" : this.getHours(),   //hour
	"m+" : this.getMinutes(), //minute
	"s+" : this.getSeconds(), //second
	"q+" : Math.floor((this.getMonth()+3)/3),  //quarter
	"S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)) format=format.replace(RegExp.$1,
						  (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    for(var k in o)if(new RegExp("("+ k +")").test(format))
	format = format.replace(RegExp.$1,
				RegExp.$1.length==1 ? o[k] :
				("00"+ o[k]).substr((""+ o[k]).length));
    return format;
}

Date.prototype.pattern=function(fmt) {         
    var o = {         
    "M+" : this.getMonth()+1, //月份         
    "d+" : this.getDate(), //日         
    "h+" : this.getHours()%12 == 0 ? 12 : this.getHours()%12, //小时         
    "H+" : this.getHours(), //小时         
    "m+" : this.getMinutes(), //分         
    "s+" : this.getSeconds(), //秒         
    "q+" : Math.floor((this.getMonth()+3)/3), //季度         
    "S" : this.getMilliseconds() //毫秒         
    };         
    var week = {         
    "0" : "\u65e5",         
    "1" : "\u4e00",         
    "2" : "\u4e8c",         
    "3" : "\u4e09",         
    "4" : "\u56db",         
    "5" : "\u4e94",         
    "6" : "\u516d"        
    };         
    if(/(y+)/.test(fmt)){         
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));         
    }         
    if(/(E+)/.test(fmt)){         
        fmt=fmt.replace(RegExp.$1, ((RegExp.$1.length>1) ? (RegExp.$1.length>2 ? "\u661f\u671f" : "\u5468") : "")+week[this.getDay()+""]);         
    }         
    for(var k in o){         
        if(new RegExp("("+ k +")").test(fmt)){         
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));         
        }         
    }         
    return fmt;         
}       

function getUrlParam(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
    var r = window.location.search.substr(1).match(reg); 
    if (r != null){ 
	return decodeURI(r[2]); 
    }
    return null; 
}

function getNowTime(){
    var now = new Date();
    var year = now.getFullYear();  
    var month = now.getMonth()+1;  
    var day = now.getDate();
    var d = year + "-" + month + "-" + day;
    return d;
}

var map;
var overlay;
var projection;
var markerClusterer;
var lineClusterer;
var stoped = true;

var line_data, circle_data, ts_series, statistics_data;

var mapWeibo = {
    infos: [],
    getPresentTopic: (getUrlParam('topic')==null)?'':getUrlParam('topic'),
    getPresentCollection: (getUrlParam('collection')==null)?'user_statuses':getUrlParam('collection'),
    step_sum : (getUrlParam('timeInterval')==null)?25:getUrlParam('timeInterval'),       //规定slider的步数总和
    starttime: (getUrlParam('starttime')==null)?'2012-01-01':getUrlParam('starttime'), 
    endtime: (getUrlParam('endtime')==null)?getNowTime():getUrlParam('endtime'),
	section: (getUrlParam('section')==null)?24:getUrlParam('section'),
	alertcoe: (getUrlParam('alertcoe')==null)?90:getUrlParam('alertcoe'),
	incremental: (getUrlParam('incremental')==null)?'1':getUrlParam('incremental'),
	width: 0.2,//if fipost == repost*(1 +- width)
    now_step : 0,
    total_number : 0,
    real_number : 0,
    max_number: 40000,
    min_number:100,
    inter_slider : null,
    interval_time : 5000,
    initialOptions : {
        zoom : 4,
	minZoom : 3,
        center: new google.maps.LatLng(35.563611,103.36388611),
        mapTypeId: google.maps.MapTypeId.ROADMAP,//SATELLITE,
        navigationControlOptions : {
            style: google.maps.NavigationControlStyle.ZOOM_PAN,
            position: google.maps.ControlPosition.TOP_LEFT
        },
        mapTypeControlOptions : {
            style : google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
	overviewMapControl : true,
	overviewMapControlOptions : {
	    opened : true,
	    position: google.maps.ControlPosition.BOTTOM_LEFT
	},
	panControl : true,
	panControlOptions : {
	    position : google.maps.ControlPosition.TOP_LEFT,
	},
	rotateControl : true,
	rotateControlOptions : {
	    position: google.maps.ControlPosition.TOP_CENTER, 
	}
    },
    reset : function () {
        map.panTo(mapWeibo.initialOptions.center);
        map.setZoom(mapWeibo.initialOptions.zoom);
    },    
    markerIcons: {
        fipost : {
            '1' : ['/static/mapweibo/images/map/markers/fipost/1.png'],
            '2' : ['/static/mapweibo/images/map/markers/fipost/2.png'],
            '3' : ['/static/mapweibo/images/map/markers/fipost/3.png']
        },
	equalpost : {
            '1' : ['/static/mapweibo/images/map/markers/equalpost/1.png'],
            '2' : ['/static/mapweibo/images/map/markers/equalpost/2.png'],
            '3' : ['/static/mapweibo/images/map/markers/equalpost/3.png']
        },
        repost : {
            '1': ['/static/mapweibo/images/map/markers/repost/1.png'],
            '2': ['/static/mapweibo/images/map/markers/repost/2.png'],
            '3': ['/static/mapweibo/images/map/markers/repost/3.png']
        },
    },
    markersByCategory : {
        fipost : [],
	equalpost: [],
        repost : []
    },
    clearMarkersByCategory : function (category) {
	mapWeibo.markersByCategory['fipost'] = [];
	mapWeibo.markersByCategory['equalpost'] = [];
	mapWeibo.markersByCategory['repost'] = [];
    },
    showMarkersByCategory : function (category) {
        for (var k=0; k<mapWeibo.markersByCategory[category].length; k+=1) {
	    var thisMarker = mapWeibo.markersByCategory[category][k];
            mapWeibo.markersByCategory[category][k].setVisible(true);
	    markerClusterer.addMarker(thisMarker);
        }
	markerClusterer.resetViewport();
        markerClusterer.redraw();
    },
    hideMarkersByCategory : function (category) {
        for (var i=0; i<mapWeibo.markersByCategory[category].length; i+=1) {
            var thisMarker = mapWeibo.markersByCategory[category][i];
            thisMarker.setVisible(false);
            markerClusterer.removeMarker(thisMarker);
        }
        markerClusterer.resetViewport();
        markerClusterer.redraw();
    },
};

var DOM = {
    tooltip : {
        inDOM: false,
        isHidden: false,
        append: function (element, content) {
            if (!this.inDOM && !this.isHidden) {
                var HTMLTooltip = '<div id="tooltip"><div class="inner">' + content + '</div></div>';
                $('body').append(HTMLTooltip);
                $('#tooltip').css({
                    top: $(element).offset().top - 47 + 'px'
                });
                this.move(element);
                this.inDOM = true;
                this.isHidden = false;
            }
        },
        hide: function () {
            if (!this.isHidden) {
                $('#tooltip').addClass('hidden');
                this.isHidden = true;
            }
        },
        move: function (element) {
            $(element).bind('mousemove', function(e){
                if (e.pageX + $('#tooltip').width()/2 < $(window).width() && e.pageX - $('#tooltip').width()/2 > 0) {
                    $('#tooltip').css({
                        left: e.pageX - ($('#tooltip').width() / 2) + 'px'
                    });
                }
            });
        },
        remove: function (element) {
            this.stop();
            $('#tooltip').remove();            
            this.inDOM = false;
            this.isHidden = false;
        },
        stop: function (element) {
            $(element).unbind('mousemove');
        }
    },
    data: [
        {
            element : '#console #categories',
            key : 'hint',
            value : '选择地图显示图标的策略.'
        }
    ],
    ui : function(){
	return{
	    init : function () {
		map = new google.maps.Map(document.getElementById('map_canvas'), mapWeibo.initialOptions);
		$('#slider').slider({
		    min: 0,
		    //max: mapWeibo.step_sum,
		    step: 1,
		});
		$('#play_pause1').button({icons: {primary: "ui-icon-play"},text: false});
		$('#play_pause2').button({icons: {primary: "ui-icon-pause"},text: false});
		$('#play_pause3').button({icons: {primary: "ui-icon-bullet"},text: false});
		if(mapWeibo.getPresentTopic != "" && mapWeibo.getPresentTopic != undefined){
		    $("#topic_input").val(mapWeibo.getPresentTopic);
		}

		if(getUrlParam("topic")!=null){				
		    $("#keywords").empty();
		    var k_html = "<p>输入<strong>筛选条件</strong>以便开始<strong>新</strong>的分析:</p><div id=\"s_keyword\"><strong>关键词:</strong><input type=\"text\" name=\"topic\" value=" + mapWeibo.getPresentTopic + " /></div><div id=\"se_time\"><strong>起始时间:</strong><input type=\"text\" name=\"starttime\" id=\"starttime\" value=" + mapWeibo.starttime + " />&nbsp;&nbsp;<strong>终止时间:</strong><input type=\"text\" name=\"endtime\" id=\"endtime\" value=" + mapWeibo.endtime + " /></div><div id=\"hour_section\"><strong>时间粒度</strong><input type=\"text\" name=\"section\" id=\"section_input\" placeholder=\"请输入时间粒度...\" value=" + mapWeibo.section + "><strong>小时</strong></div>";
		    k_html += "<button id=\"submit\" style=\"margin-left:20px;\">分析</button>";
		    $("#keywords").append(k_html);
		}
	
		$('#starttime').datepicker({
		    changeMonth: true,
		    changeYear: true,
		    dateFormat: "yy-mm-dd",
		    
		});
		$('#endtime').datepicker({
		    changeMonth: true,
		    changeYear: true,
		    dateFormat: "yy-mm-dd",
		    
		});
	    }
	}
    }(),
    nationViewButton : function () {
        var htmlElement = '<p id="back-to-nation-view" class="hidden"><span>返回到全景模式</span></p>';
        var $element;
        return {
            init : function () {
		$element = $('#mapContainer').append(htmlElement).find('#back-to-nation-view');
                $element.bind('click', function () {
                    mapWeibo.reset();
                });
		$element.removeClass('hidden');
            },
            hide : function () {
                $element.addClass('hidden');
            },
            show : function () {
                $element.removeClass('hidden');
            }
        };
    }(),
    init : function () {
	DOM.nationViewButton.init();
	DOM.ui.init();
        $('#console ul li').addClass('active').bind('click', infoWindow.close);
        $(window).bind('resize', function () {
            infoWindow.close();
        });
        $('#console #helpers li#all').bind('click', function () {
	    if(stoped == true){
		var $liAll = $(this);
		if ( !$liAll.hasClass('active') ) {
                    $('#console #categories li:not(.active)').each(function () {
			mapWeibo.showMarkersByCategory( $(this).addClass('active').attr('id') );
                    });
                    $liAll.addClass('active');
		    $('#slider').slider("option", "disabled", false);
		    $('#play_pause1').button("option", "disabled", false);
		    $('#play_pause2').button("option", "disabled", false);
		    $('#play_pause3').button("option", "disabled", false);
		}
	    }
        });
        $('#console #categories li').bind('click', function () {
	    if(stoped == true){
		var $li = $(this);
		var $liAll = $('#console #helpers li#all');
		if ( $liAll.hasClass('active') ) {
                    $li.siblings('li').each(function () {
			mapWeibo.hideMarkersByCategory( $(this).removeClass('active').attr('id') );
                    });
                    $liAll.removeClass('active');
		    $('#slider').slider("option", "disabled", true);
		    $('#play_pause1').button("option", "disabled", true);
		    $('#play_pause2').button("option", "disabled", true);
		    $('#play_pause3').button("option", "disabled", true);
		} else if ( !$li.hasClass('active') ) {
                    mapWeibo.hideMarkersByCategory( $li.siblings('li.active').removeClass('active').attr('id') );
                    mapWeibo.showMarkersByCategory( $li.addClass('active').attr('id') );
		    $('#slider').slider("option", "disabled", true);
		    $('#play_pause1').button("option", "disabled", true);
		    $('#play_pause2').button("option", "disabled", true);
		    $('#play_pause3').button("option", "disabled", true);
		}
	    }
        });
        for (var i=0; i<DOM.data.length; i+=1) {
	    var d = DOM.data[i];
	    $(d.element).data(d.key, d.value);
	    $(d.element).bind('mouseenter', function(){
		if(stoped == true){
		    DOM.tooltip.append(this, $(this).data('hint'));
		}
		else{
		    DOM.tooltip.append(this, '请先暂停播放.');
		}
	    });
	    $(d.element).bind('click', function(){
		if(stoped == true){
		    DOM.tooltip.hide();
		}
	    });
	    $(d.element).bind('mouseleave', function(){
		DOM.tooltip.remove(d.element);
	    });
        }
    }
};

function pageFailure(error){
    return;
}

function initialize() {
	$("#data").tabs({collapsible:true});
    window.location.href = "#s_keyword";
    if(!getUrlParam('topic')){
	return;
    }
    $.ajax({
	url: "/mapweibo/mapcount?topic=" + mapWeibo.getPresentTopic + "&starttime=" + mapWeibo.starttime + "&endtime=" + mapWeibo.endtime + '&section=' + mapWeibo.section + '&alertcoe=' + mapWeibo.alertcoe,
	dataType: 'json',   
	type: "GET",   
	success: function (data) {
	    mapWeibo.total_number = data.whole_count;
	    mapWeibo.real_number = data.count;
	    $("#total_number").val(mapWeibo.total_number);
	    $("#real_number").val(mapWeibo.real_number);
	}
    });
    for (var x in mapWeibo.markerIcons) {		
	for (var y in mapWeibo.markerIcons[x]) {
            mapWeibo.markerIcons[x][y][0] = new google.maps.MarkerImage(mapWeibo.markerIcons[x][y][0],
					new google.maps.Size(40, 40),
					new google.maps.Point(0, 0), // origin
					new google.maps.Point(20, 20) // anchor
				);
	}
    }
    markerClusterer = new MarkerClusterer(map, [], {
		imagePath: '/static/mapweibo/images/map/clusters/',
		gridSize: 30,
		maxZoom: 9
    });
    $("#mapContainer").block({
	message: '<h2><img src="/static/mapweibo/images/ajax_loader.gif" />数据加载中,请稍候...</h2>'
    });
    var request = '/mapweibo/mapview?topic=' + mapWeibo.getPresentTopic + '&starttime=' + mapWeibo.starttime + '&endtime=' + mapWeibo.endtime + "&collection=" + mapWeibo.getPresentCollection + '&section=' + mapWeibo.section + '&alertcoe=' + mapWeibo.alertcoe + '&incremental=' + mapWeibo.incremental;
    $.ajax({
		  url: request,
		  dataType: 'json',   
		  type: "POST",   
		  success: function (data) {
				line_data = data.line;
				circle_data = data.circle;
				ts_series = data.ts_series;
				mapWeibo.step_sum = ts_series.length;
				$('#slider').slider({
					max: mapWeibo.step_sum + 1
				})
				alert_data = data.alert;
				max_repost_num = data.max_repost_num;
				statistics_data = data.statistics_data;
				var each_step = parseInt(max_repost_num/3);
				line_blue.innerText = '0--' + each_step.toString();
				line_yellow.innerText = each_step.toString() + '--' + 2*each_step.toString();
				line_red.innerText = 2*each_step.toString()+ '--'+ max_repost_num.toString();
				
				initial_now_step();
				
				$('#slider').bind('slidechange', function(event, ui) {
					if(lineClusterer != undefined){
						lineClusterer.clearlines();
					}
					if(markerClusterer != undefined){
						markerClusterer.clearMarkers();
					}
					
					var now_slider =  $('#slider').slider( "option", "value" );
					//console.log(now_slider);
					if(now_slider == 0){
						mapWeibo.now_step = -1;
					}
					else{
						mapWeibo.now_step = now_slider - 1;
					}
					if(mapWeibo.now_step == mapWeibo.step_sum){
						date_div.innerText='当前时间';
						trend_url = "http://idec.buaa.edu.cn/mapweibo/trendview?topic=" + mapWeibo.getPresentTopic;
						network_url = "http://idec.buaa.edu.cn/retweetmap?q=" + mapWeibo.getPresentTopic+'&t=demo';
						var $dialog = $('<div></div>')
						.html('<div><span>是否查看:</span><p><a href='+trend_url+' target="_blank">话题数量趋势</a></br></br><a href='+network_url+' target="_blank">话题转发网络</a></p></div>')
						.css({'font-size': '18px','color': 'blue'})
						.dialog({
							close: function(event, ui) {$('#slider').slider( "option", "value", 0);},
							autoOpen: false,
							title: '播放结束',
							modal:true,
							draggable: false,
							resizable: false
						});
						$dialog.dialog('open');
						// setTimeout(function(){$dialog.dialog("close")},10000);
					}
					
					change_date_display();
					change_data_display();
					change_map_display();
					
				})
					
				MyOverlay.prototype = new google.maps.OverlayView();
				MyOverlay.prototype.onAdd = function() { };
				MyOverlay.prototype.onRemove = function() { };
				MyOverlay.prototype.draw = function() {
					projection = overlay.getProjection();
				};
				function MyOverlay(map) { 
					this.setMap(map); 
				}
				overlay = new MyOverlay(map);
				$("#mapContainer").unblock();
				if (stoped==true) {
					stoped = false;					
					mapWeibo.inter_slider = setInterval(play_interval, mapWeibo.interval_time);
				}
	     	},
			error: function(jqXHR, textStatus, errorThrown) {
				pageFailure("mapview_broken_down");
			}
    });
	
	$('#play_pause1').click(function() {
		if (stoped==true) {	  
			stoped = false;
			mapWeibo.inter_slider=setInterval(play_interval, mapWeibo.interval_time);
		}
    });
    $('#play_pause2').click(function() {stoped = true;});
    $('#play_pause3').click(function() {
		stoped = true;
		date_div.innerText = '';
		$('#slider').slider( "option", "value", 0);	
    });
	
    function initial_now_step(){
		mapWeibo.now_step = -1;
	}
	
    function change_date_display(){
	  if (ts_series[mapWeibo.now_step]){
		  date_div.innerText= '第' + String(mapWeibo.now_step+1) + '步' + new Date(ts_series[mapWeibo.now_step][0]*1000).pattern('yyyy-MM-dd EEE hh:mm:ss') ;//String(ts_series[mapWeibo.now_step][0])
	  }
	  else{
		  date_div.innerText = '当前时间';
	  }
    }

    function change_data_display(){
		$("#lbody").empty();
		$("#lbody").append("<tr><td><span class=\"title\" style=\"opacity: 1; \">" + '省份' + "</span></td><td><span class=\"absolute\" style=\"opacity: 1; \">" + '本期' + "</span></td><td><span class=\"incre\" style=\"opacity: 1; \">" + '增长' + "</span></td></tr>");
		$("#mbody").empty();
		$("#mbody").append("<tr><td><span class=\"title\" style=\"opacity: 1; \">" + '省份' + "</span></td><td><span class=\"absolute\" style=\"opacity: 1; \">" + '本期' + "</span></td><td><span class=\"incre\" style=\"opacity: 1; \">" + '增长' + "</span></td></tr>");
		$("#rbody").empty();
		$("#rbody").append("<tr><td><span class=\"title\" style=\"opacity: 1; \">" + '省份' + "</span></td><td><span class=\"absolute\" style=\"opacity: 1; \">" + '本期' + "</span></td><td><span class=\"incre\" style=\"opacity: 1; \">" + '增长' + "</span></td></tr>");
		if(statistics_data[mapWeibo.now_step]){ 
		  var s_data = statistics_data[mapWeibo.now_step];
		  for(var category=0;category < s_data.length;category++){
			var province_list = s_data[category];
			for(var i=0;i<province_list.length;i++){
				province = province_list[i][0];
				data = province_list[i][1];
				cur_value = data[0];
				incre_value = data[1];
				zero_status = data[2];
				if(category == 0){
					html = "<tr><td><span class=\"title\" style=\"opacity: 1; \"><a href=\"#\" >" + province + "</a></span></td><td><span class=\"absolute\" style=\"opacity: 1; \">" + cur_value + "</span></td>";
					if(zero_status == 1)
						html += "<td><span class=\"incre redline\" style=\"opacity: 1; \">" + incre_value + "</span></td></tr>";
					else
						html += "<td><span class=\"incre greenline\" style=\"opacity: 1; \">" + incre_value + "</span></td></tr>";
					$("#mbody").append(html);
				}
				if(category == 1){
					html = "<tr><td><span class=\"title\" style=\"opacity: 1; \"><a href=\"#\" >" + province + "</a></span></td><td><span class=\"absolute\" style=\"opacity: 1; \">" + cur_value + "</span></td>";
					if(zero_status == 1)
						html += "<td><span class=\"incre redline\" style=\"opacity: 1; \">" + incre_value + "</span></td></tr>";
					else
						html += "<td><span class=\"incre greenline\" style=\"opacity: 1; \">" + incre_value + "</span></td></tr>";
					$("#lbody").append(html);
				}
				if(category == 2){
					html = "<tr><td><span class=\"title\" style=\"opacity: 1; \"><a href=\"#\" >" + province + "</a></span></td><td><span class=\"absolute\" style=\"opacity: 1; \">" + cur_value + "</span></td>";
					if(zero_status == 1)
						html += "<td><span class=\"incre redline\" style=\"opacity: 1; \">" + incre_value + "</span></td></tr>";
					else
						html += "<td><span class=\"incre greenline\" style=\"opacity: 1; \">" + incre_value + "</span></td></tr>";
					$("#rbody").append(html);
				}
			}
		  }
		}
    }

    function change_map_display(){
		for(var i=0;i<mapWeibo.infos.length;i++){
			mapWeibo.infos[i].setMap(null);
		}
		mapWeibo.infos = [];
		mapWeibo.clearMarkersByCategory();
			if(markerClusterer != undefined){
			markerClusterer.clearMarkers();
			}
		if(lineClusterer != undefined){
			lineClusterer.clearlines();
		}
		var alert_series = alert_data[mapWeibo.now_step];
		//var province_name = '';
		
		var alert_text = '';
		var flag = 0;
		for(var status in alert_series){
			if(status == 'post_rsi'){
				flag = 1;
				alert_text += '总数"超买"(RSI=' + alert_series[status] + ')';
			}
			if(status == 'fipost_rsi'){
				flag = 1;
				alert_text += '原创数"超买"(RSI=' + alert_series[status] + ')';
			}
			if(status == 'repost_rsi'){
				flag = 1;
				alert_text += '转发数"超买"(RSI=' + alert_series[status] + ')';
			}
			if(status == 'repost_macd'){
				flag = 1;
				alert_text += '转发数高峰(MACD=' + alert_series[status] + ')';
			}
			if(status == 'fipost_macd'){
				flag = 1;
				alert_text += '原创数高峰(MACD=' + alert_series[status] + ')';
			}
			if(status == 'post_macd'){
				flag = 1;
				alert_text += '总数高峰(MACD=' + alert_series[status] + ')';
			}
			alert_text += ' ';
			break;
		}
		if(flag == 1){
			var date = new Date(ts_series[mapWeibo.now_step][0]*1000).format('yyyy-MM-dd');
			alert_text = date + alert_text;
			var latlng = '39.90403 116.407526';
			var split_latlng = latlng.split(' ');
			var point = new google.maps.LatLng(split_latlng[0], split_latlng[1]);
			var marker = new StyledMarker({styleIcon: new StyledIcon(StyledIconTypes.BUBBLE, {color: 'ff0000', text: alert_text}), position:point, map:map});
			mapWeibo.infos.push(marker);
		}
		
			/*province_name = alert_latlng[latlng].name;
			split_latlng = latlng.split(' ');
			var status = alert_latlng[latlng].status;
			var maxv = 0;
			var maxindex = '';
			for(key in status){
				if(maxv < status[key]){
					  maxv = status[key];
					  maxindex = key;
				}
			}
			if(maxindex == 'total'){
				maxstatus = ['微博发布总数激增', '0000ff'];
			}
			if(maxindex == 'repost'){
				maxstatus = ['微博转发总数激增', 'ffff00'];
			}
			if(maxindex == 'fipost'){
				maxstatus = ['微博原创总数激增', 'ff0000'];
			}
			point = new google.maps.LatLng(split_latlng[0], split_latlng[1]);
			var marker = new StyledMarker({styleIcon: new StyledIcon(StyledIconTypes.BUBBLE, {color: maxstatus[1], text: date+': '+province_name + maxstatus[0]}), position:point, map:map});
			mapWeibo.infos.push(marker);*/
	    
		
		
		var marker;		
		var markers = [];
		period_circle_data = circle_data[mapWeibo.now_step];
		for (var latlng in period_circle_data) {
			var count = period_circle_data[latlng];
			var fipost = count[1];
			var repost = count[0];
			var split_latlng = latlng.split(' ');
			var point = new google.maps.LatLng(split_latlng[0],split_latlng[1]);
			var category = null;
			if(fipost < repost*(1 - mapWeibo.width) || repost > fipost*(1 + mapWeibo.width))
				category = 'repost'
			else if(fipost > repost*(1 + mapWeibo.width) || repost < fipost*(1 - mapWeibo.width))
				category = 'fipost'
			else
				category = 'equalpost'
			marker = new google.maps.Marker({
				icon : mapWeibo.markerIcons[category][3][0],
				position : point,
				map : map
				});
			marker.category = category;
			marker.fipost = fipost;
			marker.repost = repost;
			markers.push(marker);
			mapWeibo.markersByCategory[category].push(marker);
			google.maps.event.addListener(marker, 'mouseover', function(){
				var marker = this;
				infoWindow.preload(marker);
				});
			google.maps.event.addListener(marker, 'mouseout', infoWindow.close);
			google.maps.event.addListener(map, 'click', infoWindow.close);
			google.maps.event.addListener(map, 'drag', infoWindow.close);
			google.maps.event.addListener(map, 'zoom_changed', function () { infoWindow.close();});
			google.maps.event.trigger(map, 'resize')
		}
		markerClusterer.addMarkers(markers, false);
		period_line_data = line_data[mapWeibo.now_step];
		lineClusterer = new LineClusterer(map, period_line_data);
	}

    function play_interval(){
		if (stoped) {
			if (mapWeibo.inter_slider!=null) {
			clearInterval(mapWeibo.inter_slider);
			}
		} 
		else {
			if (mapWeibo.now_step <= mapWeibo.step_sum  && mapWeibo.now_step >= -1) {	
				$("#slider" ).slider("option", "value", ($("#slider" ).slider("option", "value") + 1));
			}
			/*
			if(mapWeibo.now_step == mapWeibo.step_sum){	
				$("#slider" ).slider("option", "value", (mapWeibo.now_step+1));
			}*/
		}
    }
	window.location.href = "#s_keyword";
}

$(function(){
    DOM.init();
    infoWindow.init();
    initialize();	
});
