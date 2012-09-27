var collection = (getUrlParam("collection")==null)?"user_statuses":getUrlParam("collection");
// JavaScript Document
function getUrlParam(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
    var r = window.location.search.substr(1).match(reg); 
    if (r != null){ 
	return decodeURI(r[2]); 
    }
    return null; 
}
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
google.load('visualization', '1', {packages:['table','annotatedtimeline','corechart']});
$(document).ready(function() {
    if(getUrlParam("module") == "increase"){//进入统计增长最快的省份模式
	var province = getUrlParam("province");
	var starttime = new Date(parseInt(getUrlParam("starttime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	var endtime = new Date(parseInt(getUrlParam("endtime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	var p_starttime;
	var p_endtime;
	if(getUrlParam("p_starttime") != null && getUrlParam("p_endtime") != null){
	    p_starttime = new Date(parseInt(getUrlParam("p_starttime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	    p_endtime = new Date(parseInt(getUrlParam("p_endtime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	    $("#main").append("<h2>" + province + " 上一时间段（从" + p_starttime + "到" + p_endtime + "）微博</h2><div id='pre_weibo_table'></div>");
	}
	else{
	    $("#main").append("<h2>本时间段为所选时间起点</h2>");
	    //$("#main").append("<h2>" + province + " 上一时间段微博</h2><div id='pre_weibo_table'></div>");
	}
	
	$("#main").append("<h2>" + province + " 本时间段（从" + starttime + "到" + endtime + "）微博</h2><div id='weibo_table'></div>");
	var idlist = getUrlParam("idlist");
	if(idlist){
	    $.ajax({
		url:'/mapweibo/mapview/text?idlist=' + getUrlParam("idlist") + '&collection=' + collection,
		dataType:'json',
		success:function(data){
		    //drawpie(data);
		    drawweibotable(data,'weibo_table');
		    
		}
	    });
	}
	var preidlist = getUrlParam("preidlist");
	//console.log(preidlist);
	if(preidlist != 'null' && preidlist != null){
	    $.ajax({
		url:'/mapweibo/mapview/text?idlist=' + preidlist + '&collection=' + collection,
		dataType:'json',
		success:function(data){
		    drawweibotable(data,'pre_weibo_table');
		}
	    });
	}
	else{
	    $('#pre_weibo_table').append("<h3>本地区上一时间段无没有搜索到微博</h3>");
	}
    }
    else if(getUrlParam("module") == "static"){//进入累计统计模式
	
	var idlist = getUrlParam("idlist");
	var _idlist = idlist.split(" ");
	var starttime = new Date(parseInt(getUrlParam("starttime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	var endtime = new Date(parseInt(getUrlParam("endtime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	var status; 
	var province = getUrlParam("province");
	var p_s = getUrlParam('status');
	
	if(p_s == 'fipost'){
	    status = '原创';
	}
	else if(p_s == 'repost'){
	    status = '转发';
	}
	else{
	    status = '所有（包括原创和转发）';
	}
	

	$("#main").append("<h3>" + province + " 从" + starttime + "到" + endtime + "的累计" + status + "微博</h3></div><div id='weibo_table'></div>");
	/*<div id='timeline' style='height: 500px; min-width: 500px'>
	  if(_idlist.length > 10){//如果微博数量大于阀值，则展示时间分布曲线
	  $.getJSON('/getText?idlist=' + getUrlParam("idlist") + "&module=" + getUrlParam("module"),function(data){
	  //drawpie(data);
	  console.log(data);
	  window.chart = new Highcharts.StockChart({
	  chart: {
	  renderTo: 'timeline',
	  borderWidth: 1,
	  width:970,
	  //height: 200
	  },
	  navigator: {
	  enabled: false
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
	  
	  
	  },
	  
	  xAxis: {
	  type:"datetime",
	  maxPadding:0.05,
	  minPadding:0.05,
	  tickInterval: 24*3600*1000*1,
	  dateTimeLabelFormats:
	  {
	  second: '%H:%M:%S',
	  //minute: '%e. %b %H:%M',
	  //hour: '%b/%e %H:%M',
	  day: '%e/%b/%y',
	  //week: '%e. %b',
	  //month: '%b %y',
	  //year: '%Y'
	  }
	  },
	  
	  title: {
	  text: '微博数量的时间分布曲线'
	  },
	  
	  subtitle: {
	  text: '',//'话题：' +  $("#select_topic").val()  // dummy text to reserve space for dynamic subtitle
	  },
	  
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
	  
	  series: {
	  name:'',
	  data:data
	  }
	  });
	  });
	  }*/
	if(idlist){
	    $.ajax({
		url:'/mapweibo/mapview/text?idlist=' + getUrlParam("idlist") + '&collection=' + collection,
		dataType:'json',
		success:function(data){
		    //drawpie(data);
		    drawweibotable(data,'weibo_table');
		    
		}
	    });
	}
    }
    else{
	if(getUrlParam("starttime") != null && getUrlParam("endtime") != null){
	    var starttime = new Date(parseInt(getUrlParam("starttime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	    var endtime = new Date(parseInt(getUrlParam("endtime"))*1000).format('yyyy-MM-dd hh:mm:ss');
	}
	var province = getUrlParam("province");
	var idlist = getUrlParam("idlist");
	$("#main").append("<h3>" + province + " 本时间段（从" + starttime + "到" + endtime + "）微博</h3><div id='weibo_table'></div>");
	if(idlist){
	    $.ajax({
		url:'/mapweibo/mapview/text?idlist=' + getUrlParam("idlist") + '&collection=' + collection,
		dataType:'json',
		success:function(data){
		    //drawpie(data);
		    drawweibotable(data,'weibo_table');

		}
	    });
	}
    }
    
    
    function drawweibotable(serverData,container_id){
	var weibodata = serverData;
	/*
	  for(var i = 0;i < serverData.length;i = i + 1){
	  new10data.push(serverData[i]);
	  } 
	*/
	var data = new google.visualization.DataTable();
	
	data.addColumn('string', '用户id');
	data.addColumn('string', '微博id');
	data.addColumn('string', '发布时间');
	data.addColumn('string', '用户位置');
	data.addColumn('string', '用户姓名');
	data.addColumn('string', '状态');
        data.addColumn('string', '文本');
	data.addColumn('string', '话题标签'); 
	data.addRows(weibodata);
	//data.setCell(4, 2, 15, 'Fifteen', {style: 'font-style:bold; font-size:22px;width:10px'});
	var tableforweibo = new google.visualization.Table(document.getElementById(container_id));
	tableforweibo.draw(data, {showRowNumber: true}); 
    }
});

/*
  function drawpie(serverData){
  var weibodata = serverData;
  var result = [["发布状态","比例"]];
  for(var i = 0;i < data[2].length;i = i + 1){
  result.push(data[2][i]);
  }
  var da = google.visualization.arrayToDataTable(result);
  
  var options = {
  title: data[1] + data[0],
  chartArea:{left:10,
  top:50},
  legend:{
  position:'none'},
  fontSize:12,
  height: 170,
  width: 150
  };
  var emotion_chart = new google.visualization.PieChart(document.getElementById("weibo_pie"));
  //console.log(emotion_chart);
  //console.log(da);
  emotion_chart.draw(da, options);
  }*/