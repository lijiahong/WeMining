d_weibo = [];   
 
for(var i=0; i<250; ++i){
    d_weibo.push(null);
}

d_user = [];   
 
for(var i=0; i<250; ++i){
    d_user.push(null);
}

var real_weibo_count = [];

function getWeiboGraph(id, d){
    var graph = new RGraph.Line(id, d);
    graph.Set('chart.xticks', 100);
    graph.Set('chart.background.barcolor1', 'white');
    graph.Set('chart.title.xaxis', '时间 >>>');
    //graph.Set('chart.title.yaxis', '效率 (条数/10s)');
    graph.Set('chart.title.vpos', 0.5);
    //graph.Set('chart.title.yaxis.pos', 1.25);
    graph.Set('chart.title.xaxis.pos', 0.5);
    graph.Set('chart.filled', true);
    graph.Set('chart.fillstyle', ['#faa']);
    graph.Set('chart.colors', ['red']);
    graph.Set('chart.linewidth', 1);
    graph.Set('chart.yaxispos', 'right');
    graph.Set('chart.ymax', 4000);
    graph.Set('chart.xticks', 25);
    return graph;
}

function getUserGraph(id, d){
    var graph = new RGraph.Line(id, d);
    graph.Set('chart.xticks', 100);
    graph.Set('chart.background.barcolor1', 'white');
    graph.Set('chart.title.xaxis', '时间 >>>');
    //graph.Set('chart.title.yaxis', '效率 (条数/10s)');
    graph.Set('chart.title.vpos', 0.5);
    //graph.Set('chart.title.yaxis.pos', 1.25);
    graph.Set('chart.title.xaxis.pos', 0.5);
    graph.Set('chart.filled', true);
    graph.Set('chart.fillstyle', ['#faa']);
    graph.Set('chart.colors', ['red']);
    graph.Set('chart.linewidth', 1);
    graph.Set('chart.yaxispos', 'right');
    graph.Set('chart.ymax', 200);
    graph.Set('chart.xticks', 25);
    return graph;
}

function drawIncrementalGraph(){
    RGraph.Clear(document.getElementById("weibo_cvs"));
    RGraph.Clear(document.getElementById("user_cvs"));
    var weibo_graph = getWeiboGraph('weibo_cvs', d_weibo);
    var user_graph = getUserGraph('user_cvs', d_user);
    weibo_graph.Draw();
    user_graph.Draw();
    // Add some data to the data arrays
    jQuery.ajax({
    	url: "/api/spider/count.json",
    	type: "GET",
    	success: function(data){
    	    data = ''+data
            total_count = data.split(';')[0];
            target_count = data.split(';')[1]; 
    	    $("#total_count").html('抓取weibo总数:'+total_count);
    	    $("#target_count").html('抓取user总数:'+target_count);
    	    d_weibo.push(total_count-weibo_count);
            d_user.push(target_count-user_count);
    	    weibo_count = total_count;
            user_count = target_count;
    	}
    });
    if(d_weibo.length > 250){
        d_weibo = RGraph.array_shift(d_weibo);
    }
    if(d_user.length > 250){
        d_user = RGraph.array_shift(d_user);
    }
    if(document.all && RGraph.isIE8()){
        alert('[MSIE] Sorry, Internet Explorer 8 is not fast enough to support animated charts');
    }else{
        setTimeout(drawIncrementalGraph,10000);
        // This is an alternative to setTimeout() which uses the newer requestAnimationFrame() function
        //RGraph.Effects.UpdateCanvas(drawGraph);
    }
}

var total_count;
var target_count;
var weibo_count;
var user_count;
$.ajax({
    url: "/api/spider/count.json",
    type: "GET",
    success: function(data){
        data = ''+data
    	total_count = data.split(';')[0];
    	target_count = data.split(';')[1];
    	weibo_count = total_count;
        user_count = target_count;
        $("#total_count").html('抓取微博总数:'+total_count);

    	$("#target_count").html('抓取用户总数:'+target_count);
        drawIncrementalGraph();
        //setInterval(display_realtime_graph, 1000);
        display_realtime_weibo();
        display_realtime_user();
    }
});

var MAX_POINT = 30;
var TIMEOUT = 2000;

function display_realtime_weibo(){
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    var chart_obj = $('#weibo_container').highcharts({
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function() {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    var max_point = 60;
                    window.setInterval(function(){
                        var x = (new Date()).getTime();
                        var isShift = series.data.length > MAX_POINT;
                        series.addPoint([x , parseInt(total_count)], true, isShift);//当series中Point数量超过指定值，设定isShift为true，就可以移除第一个Point，防止浏览器内存占用太大无响应

                    }, TIMEOUT);
                }
            }
        },
        title: {
            text: '实时weibo监测'
        },
        xAxis: {
            title: {
                enabled: true,
                text: '时间'
            },
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '数量（每隔10s刷新一次）'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+ this.y + '条';
            }
        },
        legend: {
           layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -20,
            y: 0,
            borderWidth: 1,
            enabled: true
        },
        exporting: {
            enabled: true
        },
        series: [{
            name: 'weibo条数',
            data: [{
                x: (new Date()).getTime(),
                y: parseInt(total_count)
            }]
        }]
    });
}

function display_realtime_user(){
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    var chart_obj = $('#user_container').highcharts({
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function() {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    var max_point = 60;
                    window.setInterval(function(){
                        var x = (new Date()).getTime();
                        var isShift = series.data.length > MAX_POINT;
                        series.addPoint([x , parseInt(target_count)], true, isShift);//当series中Point数量超过指定值，设定isShift为true，就可以移除第一个Point，防止浏览器内存占用太大无响应

                    }, TIMEOUT);
                }
            }
        },
        title: {
            text: '实时user监测'
        },
        xAxis: {
            title: {
                enabled: true,
                text: '时间'
            },
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '数量（每隔10s刷新一次）'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+ this.y + '人';
            }
        },
        legend: {
           layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -20,
            y: 0,
            borderWidth: 1,
            enabled: true
        },
        exporting: {
            enabled: true
        },
        series: [{
            name: 'user人数',
            data: [{
                x: (new Date()).getTime(),
                y: parseInt(target_count)
            }]
        }]
    });
}

