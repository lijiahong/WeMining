function getUrlParam(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
    var r = window.location.search.substr(1).match(reg); 
    if (r != null){ 
	return decodeURI(r[2]); 
    }
    return null; 
}

function getNumber(topic, collection){
    var seriesOptions = [],
    yAxisOptions = [],
    seriesCounter = 0,
    names = ['total'],
    colors = Highcharts.getOptions().colors;

    $.each(names, function(i, name) {
	$.getJSON('/mapweibo/trendnum?topic=' + topic + '&filename=' + name + '&collection=' + collection,    function(data) {
	    
		seriesOptions[i] = {
		name: name,
		data: data,
		//pointInterval: 3600 * 1000,
	    };

	    // As we're loading the data asynchronously, we don't know what order it will arrive. So
	    // we keep a counter and create the chart when all the data is loaded.
	    seriesCounter++;

	    if (seriesCounter == names.length) {
		$("loading").css("display", "none");
		createChart();
		//$("#timedist").unblock();
	    }
	});
    });
    // create the chart when all data is loaded
    function createChart() {

	chart = new Highcharts.StockChart({
	    chart: {
		renderTo: 'timedist',
		borderWidth: 1,
		//width:840,
		//height: 200
		borderColor:"#ffffff"
	    },

	    rangeSelector: {
		buttons: [{
		    type: 'day',
		    count: 1,
		    text: '1d'
		}, {
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
		    type: 'ytd',
		    text: 'YTD'
		}],
		selected: 5
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

	    xAxis: {
		type:"datetime",
		maxPadding:0.05,
		minPadding:0.05,
		//tickInterval: 24*3600*1000*1,
		dateTimeLabelFormats:
		{
		    //second: '%H:%M:%S',
		    //minute: '%e. %b %H:%M',
		    //hour: '%b/%e %H:%M',
		    day: "%b'%e",
		    //week: '%e. %b',
		    //month: '%b %y',
		    //year: '%Y'
		}
	    },
	    
	    title: {
		text:  topic + '事件'
	    },
	    /*
	      subtitle: {
	      text: '话题：' +  topic  // dummy text to reserve space for dynamic subtitle
	      },
	    */
	    
	    plotOptions: {
		series: {
		    //compare: 'value'
		}
	    },
	    
	    tooltip: {
		pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> <br/>',
		xDateFormat: '%d/%m/%Y %H:%M:%S',
		valueDecimals: 2,
	    },
	    
	    series: seriesOptions
	});
    }
    
}
function time2date(ts){
	var mydate = new Date(ts);
	return mydate;
}
function timeformat(ts){
	var mydate = new Date(ts);
	var day = mydate.getFullYear() + "-" + (mydate.getMonth()+1) + "-" + mydate.getDate();
	return day;
}
function drawTimeline(da){
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', '总数');
    data.addColumn('string', 'title1');
    data.addColumn('string', 'text1');
    var final_ds = [];
    for(var d = 0;d < da.length;d = d + 1){
		var time = da[d][0];
		var date = time2date(time);
		
		if(timeformat(time) == "2012-8-15"){
			final_ds.push([date,da[d][1],"event1","中国香港保钓船“启丰二号”成功登陆钓鱼岛"]);
		}
		if(timeformat(time) == "2012-8-19"){
			final_ds.push([date,da[d][1],"event2","日本１０名右翼分子当地时间１９日上午非法登上中国钓鱼岛"]);
		}
		if(timeformat(time) == "2012-8-31"){
			final_ds.push([date,da[d][1],"event3","在8月份国防部例行记者会上，国防部发言人耿雁生针对有关钓鱼岛的提问回应称，中国军队密切关注日方有关动向。对于近日外媒猜测中国正在试射东风41导弹，耿雁生未正面回应。他透露，近期在境内进行了一些正常的武器试验，试验不针对任何特定国家和目标。此外，他表示，中方欢迎美国国防部长9月中旬访华。"]);
		}
		if(timeformat(time) == "2012-9-11"){
			final_ds.push([date,da[d][1],"event4","日本内阁官房长官藤村修10日宣布，日本政府已经决定由政府购买“尖阁诸岛”(即中国钓鱼岛及其附属岛屿)中的钓鱼岛、北小岛和南小岛，将这三个岛“收归国有”。中华人民共和国政府10日就中华人民共和国钓鱼岛及其附属岛屿的领海基线发表声明。"]);
		}
		if(timeformat(time) == "2012-9-14"){
			final_ds.push([date,da[d][1],"event5","中国海监船编队抵钓鱼岛海域开展维权巡航执法"]);
		}
		if(timeformat(time) == "2012-9-18"){
			final_ds.push([date,da[d][1],"event6","九·一八，中日对阵钓鱼岛"]);
		}
		else{
			final_ds.push([date,da[d][1],undefined,undefined]);
		}
    }
    data.addRows(final_ds);
    var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('timelinedist'));
    chart.draw(data, {displayAnnotations: true,colors:['blue','red','green'],annotationsWidth:20,zoomStartTime:new Date(2012,7,1),zoomEndTime:new Date()});   
}
google.load('visualization', '1', {packages:['annotatedtimeline']});
$(document).ready(function(){
    $("#topic_input").val(getUrlParam('topic'));
	getNumber(getUrlParam('topic'), getUrlParam('collection'));
	$.ajax({
		url:'/mapweibo/trendnum?topic=' + getUrlParam('topic'),
		dataType:"json",
		success:function(data){
			drawTimeline(data);
		}
    });
});
/*$("#timedist").block({
    message: '<h2><img src="/static/mapweibo/images/ajax_loader.gif" /> Just a moment...</h2>'
});*/

