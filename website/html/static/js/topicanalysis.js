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

//set current china map section to null
var current = null;

//set emotion pie chart count
var emotion_chart_count = 0;
//set state of emotion chart
var emotion_chart_hide = 1

function getUrlParam(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
    var r = window.location.search.substr(1).match(reg); 
    if (r != null){ 
	return decodeURI(r[2]); 
    }
    return null; 
}

//设置highcharts主题
var highchartsOptions = Highcharts.setOptions(Highcharts.theme);

google.load('visualization', '1', {packages:['table','annotatedtimeline','corechart']});

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

$(document).ready(function() {
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
    $('#result_body').css("display", "none");
    topic_name = getUrlParam('topic');
    $("#search_box")[0].value = topic_name;
    // $('#present_topic').html("当前话题：" + topic_name + " ");
    $('#present_time').html("数据源：新浪公共微博数据");
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
	url:"/topicweibo/analysis?topic="+encodeURIComponent(topic_name)+"&json=1",
	dataType:"json",
	success:function(data){
	    $('#ajax_loading').css("display", "none");
	    $('#result_body').css("display", "inline");
	    if(data['timedist'].length == 0)
		$('#information').html('当前话题还没有数据,请选择其他话题.')
	    drawTimeDist(data['timedist']);
	    drawChinamap(data['china_map_count']);
	    drawMoodTimelie(data['mood_timeline']);
	    drawMoodMost(data['mood_location']);
	}
    });
    $("#more_pie_charts").click(function() {
	if(emotion_chart_hide){
	    for(var i = 3;i <emotion_chart_count;i++){
		$("#p_emotion_"+i).show();
	    }
	    $("#more_pie_charts").text('隐藏');
	    emotion_chart_hide = 0; 
	}
	else{
	    for(var i = 3;i <emotion_chart_count;i++){
		$("#p_emotion_"+i).hide();
	    }
	    $("#more_pie_charts").text('显示更多...'); 
	    emotion_chart_hide = 1; 
	}
    });
    //fetchPublicStatuses(topic_name, 1);
});

function fetchPublicStatuses(topic_name, page){
    statuses_data = [];
    $.ajax({
	url:"/topicweibo/analysis?topic="+encodeURIComponent(topic_name)+"&public=1&json=1&page="+page,
	dataType:"json",
	success:function(data){
	    $('#statuses_ajax_loading').hide();
	    drawStatusesTable(data);
	}
    });  
}

function drawMoodTimelie(da){
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'sad');
    data.addColumn('string', 'title1');
    data.addColumn('string', 'text1');
    data.addColumn('number', 'angry');
    data.addColumn('string', 'title2');
    data.addColumn('string', 'text2');
    data.addColumn('number', 'happy');
    data.addColumn('string', 'title2');
    data.addColumn('string', 'text2');
    final_ds = [];
    for(var d = 0;d < da.length;d = d + 1){
	time = da[d][0];
	times = time.split("-");
	ti = new Date(times[0],String(parseInt(times[1]-1)),times[2]);
	final_ds.push([ti,da[d][1],undefined,undefined,da[d][2],undefined,undefined,da[d][3],undefined,undefined]);
    }
    data.addRows(final_ds);
    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('annotatedtimeline_chart_div'));
    chart.draw(data, {displayAnnotations: true,colors:['blue','red','green'],annotationsWidth:20});  
}

function drawTimeDist(data){
    var xdata_series = [];
    var value_series = [];
    for(var i = 0;i < data.length;i = i + 1){
	xdata_series.push(data[i][0]);
	value_series.push(data[i][1]);
    }
    weektimechart = new Highcharts.Chart({
	chart: {
            renderTo: 'timedist_container',
            type: 'column'
	},
	title: {
            text: '微博数量时间分布柱状图'
	},
	subtitle: {
            text: '话题：' +  topic_name
	},
	xAxis: {
            categories:  xdata_series,
            title: {
		text: null
            },
	    labels:{
		enabled:false,
	    },
	},
	yAxis: {
            min: 0,
            title: {
		text: '微博数量 (条)',
		align: 'high'
            },
            labels: {
		overflow: 'justify'
            }
	},
	tooltip: {
            formatter: function() {
		return '时间:' + this.x + ' ' +
                    this.series.name +':'+ this.y;
            }
	},
	plotOptions: {
            bar: {
		dataLabels: {
                    enabled: true
		}
            }
	},
	legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -100,
            y: 0,
            floating: true,
            borderWidth: 1,
            backgroundColor: '#FFFFFF',
            shadow: true
	},
	credits: {
            enabled: false
	},
	series: [{
            name: '微博数量',
            data: value_series
	}],
	exporting: {
            enabled: false
        }
    });
}

function drawMoodMost(emotion_data){
    emotion_timeline = emotion_data.tmline
    emotion_total_most = emotion_data.total_most
    emotion_province_dist = emotion_data.province_emotion_dist
    var date_most = [];
    date_most.push(['汇总', emotion_total_most[1][0], emotion_total_most[1][1], emotion_total_most[1][2]]);
    // date_most.push(['汇总(数量)', emotion_total_most[0][0], emotion_total_most[0][1], emotion_total_most[0][2]]);
    for(var i = 0;i < emotion_timeline.length;i = i + 1){
	date_most.push([emotion_timeline[i][0],emotion_timeline[i][1][0],emotion_timeline[i][1][1],emotion_timeline[i][1][2]]);
    }
    drawEmotionMostTable(date_most);
    emotion_chart_count = emotion_province_dist.length
    for(var i=0;i<emotion_chart_count;i+=1){
    	if(i > 2){
    	    $("#more_pie_charts").show();
    	    $("#p_emotion").append("<div id='p_emotion_" + i + "' style='display: none;width: 200px; height: 150px;'></div>");
    	    createEmotionPieChart(emotion_province_dist[i],'p_emotion_' + String(i));
    	}
    	else{
    	    $("#p_emotion").append("<div id='p_emotion_" + i + "' style='width: 200px; height: 150px;'></div>");
    	    createEmotionPieChart(emotion_province_dist[i],'p_emotion_' + String(i));
    	}
    }
    function createEmotionPieChart(data, container_id){
    	var result = [["情绪","比例"]];
    	for(var i = 0;i<data[1].length;i+=1){
	    emotions = ['悲伤', '愤怒', '高兴'];
	    result.push([emotions[i], data[1][i]]);
    	}
    	var da = google.visualization.arrayToDataTable(result);
    	var options = {
    	    title: data[0],
	    width:250,
	    height:180
    	};
    	var emotion_chart = new google.visualization.PieChart(document.getElementById(container_id));
    	emotion_chart.draw(da, options);
    }
}

function drawEmotionMostTable(serverData){
    var date_most_data = [];
    for(var i = 0;i < serverData.length;i = i + 1){
	date_most_data.push([serverData[i][0],serverData[i][1],serverData[i][2],serverData[i][3]]);
    }
    var data = new google.visualization.DataTable();
    data.addColumn('string', '日期');
    data.addColumn('string', '最悲伤省份');
    data.addColumn('string', '最愤怒省份');
    data.addColumn('string', '最高兴省份');
    data.addRows(date_most_data);
    var tableforemotion = new google.visualization.Table(document.getElementById('table_div_for_emotion'));
    tableforemotion.draw(data, {showRowNumber: false, width:600, page: 'enable', pageSize: 5}); 
}

function drawStatusesTable(statuses_data){
    var data = new google.visualization.DataTable();
    data.addColumn('string', '发布时间');
    data.addColumn('string', '用户位置');
    data.addColumn('string', '用户昵称');
    data.addColumn('string', '文本');
    data.addColumn('string', '话题标签');
    data.addRows(statuses_data);
    var statuses_table = new google.visualization.Table(document.getElementById('statuses_table_div'));
    statuses_table.draw(data, {showRowNumber: false, page: 'enable', pageSize: 10}); 
    var title = "发布时间";
    var width = "80px";
    $('.google-visualization-table-th:contains(' + title + ')').css('width', width);
    title = "用户位置";
    width = "80px";
    $('.google-visualization-table-th:contains(' + title + ')').css('width', width);
    title = "用户昵称";
    width = "80px";
    $('.google-visualization-table-th:contains(' + title + ')').css('width', width);
    title = "话题标签";
    width = "80px";
    $('.google-visualization-table-th:contains(' + title + ')').css('width', width);
}