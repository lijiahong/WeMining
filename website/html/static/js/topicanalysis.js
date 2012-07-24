//set current china map section to null
var current = null;

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

$(document).ready(function() {
    topic_name = getUrlParam('topic');
    present_topic.innerText = "当前话题：" + topic_name + " ";
    present_time.innerText = "更新时间" + (new Date()).toString();
	
    $("#submit_analysis").click(function() {
	var _topic = $$("#keyword")[0].value;
	if(_topic != undefined){
	    window.location.href="/topicweibo/analysis?topic=" + _topic;
	}
    });
    
    $.ajax({
	url:"/topicweibo/analysis?topic="+getUrlParam("topic")+"&json=1",
	dataType:"json",
	success:function(data){
	    drawWeekDist(data['timedist_week']);	
	    drawDayDist(data['timedist_day']);
	    drawRandomStatuses(data['random_statuses']);
	    drawChinamap(data['china_map_count']);
	    drawMoodTimelie(data['mood_timeline']);
	    drawMoodMost(data['mood_location']);
	}
    });
});

function drawMoodTimelie(da){
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'angry');
    data.addColumn('string', 'title1');
    data.addColumn('string', 'text1');
    data.addColumn('number', 'sad');
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
    chart.draw(data, {displayAnnotations: true,colors:['red','blue','green'],annotationsWidth:20});  
}

function drawRandomStatuses(serverData){
    var new10data = serverData;
    var data = new google.visualization.DataTable();
    data.addColumn('number', '用户id');
    data.addColumn('string', '微博id');
    data.addColumn('string', '发布时间');
    data.addColumn('string', '用户位置');
    data.addColumn('string', '用户姓名');
    data.addColumn('string', '文本');
    data.addColumn('string', '话题标签'); 
    data.addRows(new10data);
    var tablefornew10weibo = new google.visualization.Table(document.getElementById('table_div'));
    tablefornew10weibo.draw(data, {showRowNumber: true}); 
}

function drawWeekDist(data){
    var xdata_series = [];
    var value_series = [];
    for(var i = 0;i < data.length;i = i + 1){
	xdata_series.push(data[i][0]);
	value_series.push(data[i][1]);
    }
    weektimechart = new Highcharts.Chart({
	chart: {
            renderTo: 'timedistweek_container',
            type: 'bar'
	},
	title: {
            text: '微博数量周分布条形图'
	},
	subtitle: {
            text: '话题：' +  topic_name
	},
	xAxis: {
            categories:  xdata_series,
            title: {
		text: null
            }
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
		return ''+
                    this.series.name +': '+ this.y;
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
            y: 100,
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
	}]
    });
}

function drawDayDist(data){
    var value_series = [];
    var da;
    da = data[0];
    for(var i = 0;i < data[1].length;i = i + 1){
	value_series.push(data[1][i]);
    }
    daytimechart = new Highcharts.Chart({
	chart: {
            renderTo: 'timedistday_container',
            type: 'column'
	},
	title: {
            text: '微博数量日分布条形图'
	},
	subtitle: {
            text: '话题：' +  topic_name + ' 日期：' + da
	},
	xAxis: {
            categories: [
		'0-4h',
		'4-8h',
		'8-12h',
		'12-16h',
		'16-20h',
		'20-24h'
            ]
	},
	yAxis: {
            min: 0,
            title: {
		text: '微博数量 (条)'
            }
	},
	legend: {
            layout: 'vertical',
            backgroundColor: '#FFFFFF',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            shadow: true
	},
	tooltip: {
            formatter: function() {
		return ''+
                    this.x +': '+ this.y;
            }
	},
	plotOptions: {
            column: {
		pointPadding: 0.2,
		borderWidth: 0
            }
	},
        series: [{
            name: '微博数量',
            data: value_series
	}]
    });
}

function drawMoodMost(emotion_timeline){
    var date_most = [];
    var date_location_emotion = [];
    for(var i = 0;i < emotion_timeline.length;i = i + 1){
	date_most.push([new Date(emotion_timeline[i][0]),emotion_timeline[i][2][0],emotion_timeline[i][2][1],emotion_timeline[i][2][2]]);
	for(var j = 0;j < 3;j = j + 1){
	    if(emotion_timeline[i][2][j] != ""){
		e = [];
		e.push(["悲伤",emotion_timeline[i][1][emotion_timeline[i][2][j]][0]]);
		e.push(["愤怒",emotion_timeline[i][1][emotion_timeline[i][2][j]][1]]);
		e.push(["高兴",emotion_timeline[i][1][emotion_timeline[i][2][j]][2]]);
		date_location_emotion.push([emotion_timeline[i][0],emotion_timeline[i][2][j],e]);	
	    }
	}
	
    }
    drawEmotionMostTable(date_most);
    for(var i = 0;i < date_location_emotion.length;i = i + 1){
	$("#p_emotion").append("<div id='p_emotion_" + i + "' style='width: 320px; height: 200px;'></div>");
	createEmotionPieChart(date_location_emotion[i],'p_emotion_' + String(i));
	
    }
    function createEmotionPieChart(data,container_id){
	var result = [["情绪","比例"]];
	for(var i = 0;i < data[2].length;i = i + 1){
	    result.push(data[2][i]);
	}
	var da = google.visualization.arrayToDataTable(result);
	
	var options = {
	    title: data[1] + data[0],
	};
	var emotion_chart = new google.visualization.PieChart(document.getElementById(container_id));
	emotion_chart.draw(da, options);
    }
}

function drawEmotionMostTable(serverData){
    var date_most_data = [];
    for(var i = 0;i < serverData.length;i = i + 1){
	date_most_data.push([new Date(serverData[i][0]),serverData[i][1],serverData[i][2],serverData[i][3]]);
    }
    var data = new google.visualization.DataTable();
    data.addColumn('date', '日期');
    data.addColumn('string', '最悲伤省份');
    data.addColumn('string', '最愤怒省份');
    data.addColumn('string', '最高兴省份');
    data.addRows(date_most_data);
    var tableforemotion = new google.visualization.Table(document.getElementById('table_div_for_emotion'));
    tableforemotion.draw(data, {showRowNumber: true}); 
}