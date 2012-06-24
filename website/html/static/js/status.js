d = [];   
 
for(var i=0; i<250; ++i){
    d.push(null);
}

function getGraph(id, d){
    var graph = new RGraph.Line(id, d);
    graph.Set('chart.xticks', 100);
    graph.Set('chart.background.barcolor1', 'white');
    graph.Set('chart.title.xaxis', '时间 >>>');
    graph.Set('chart.title.yaxis', '效率 (条数/10s)');
    graph.Set('chart.title.vpos', 0.5);
    graph.Set('chart.title.yaxis.pos', 0.5);
    graph.Set('chart.title.xaxis.pos', 0.5);
    graph.Set('chart.filled', true);
    graph.Set('chart.fillstyle', ['#faa']);
    graph.Set('chart.colors', ['red']);
    graph.Set('chart.linewidth', 1);
    graph.Set('chart.yaxispos', 'right');
    graph.Set('chart.ymax', 900);
    graph.Set('chart.xticks', 25);
    return graph;
}

function drawGraph(){
    RGraph.Clear(document.getElementById("cvs"));
    var graph = getGraph('cvs', d);
    graph.Draw();
    // Add some data to the data arrays
    jQuery.ajax({
	url: "/count/",
	type: "GET",
	success: function(data){
	    //console.log(data-count)
            total_count = data.split(';')[0];
            target_count = data.split(';')[1]; 
	    $("#total_count").html('抓取总数:'+total_count);
	    $("#target_count").html('目标用户抓取总数:'+target_count);
	    d.push(total_count-count);
	    count = total_count;
	}
    });
    if(d.length > 250){
        d = RGraph.array_shift(d);
    }
    if(document.all && RGraph.isIE8()){
        alert('[MSIE] Sorry, Internet Explorer 8 is not fast enough to support animated charts');
    }else{
        setTimeout(drawGraph,10000);
        // This is an alternative to setTimeout() which uses the newer requestAnimationFrame() function
        //RGraph.Effects.UpdateCanvas(drawGraph);
    }
}

var count;
$.ajax({
    url: "/count/",
    type: "GET",
    success: function(data){
	total_count = data.split(';')[0];
	target_count = data.split(';')[1];
	count = total_count;
        $("#total_count").html('抓取总数:'+total_count);
	$("#target_count").html('目标用户抓取总数:'+target_count);
        drawGraph();
    }
});