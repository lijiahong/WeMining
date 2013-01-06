var chartData1 = [];
var chart1;
function generateChartData1() {
	/*
	var firstDate = new Date(2012, 0, 1);
	firstDate.setDate(firstDate.getDate() - 500);
	firstDate.setHours(0, 0, 0, 0);

	for (var i = 0; i < 500; i++) {
		var newDate = new Date(firstDate);
		newDate.setDate(newDate.getDate() + i);

		var a = Math.round(Math.random() * (40 + i)) + 100 + i;
		var b = Math.round(Math.random() * 100000000);

		chartData1.push({
			date: newDate,
			value: a,
			volume: b
		});
	}*/
	chartData1 = [{date: new Date(2011, 11, 14), value: 1}, {date: new Date(2012, 6, 1), value: 1}, {date: new Date(2012, 8, 31), value: 1}, {date: new Date(2012, 9, 19), value: 145}, {date: new Date(2012, 9, 20), value: 60}, {date: new Date(2012, 9, 21), value: 52}, {date: new Date(2012, 9, 22), value: 56}, {date: new Date(2012, 9, 23), value: 92}, {date: new Date(2012, 9, 24), value: 67}, {date: new Date(2012, 9, 25), value: 11}, {date: new Date(2012, 9, 26), value: 3}, {date: new Date(2012, 9, 27), value: 18}, {date: new Date(2012, 9, 29), value: 10}, {date: new Date(2012, 9, 30), value: 3}, {date: new Date(2012, 10, 01), value: 3}, {date: new Date(2012, 10, 02), value: 4}, {date: new Date(2012, 10, 03), value: 2}, {date: new Date(2012, 10, 04), value: 14}, {date: new Date(2012, 10, 05), value: 2}, {date: new Date(2012, 10, 06), value: 3}, {date: new Date(2012, 10, 07), value: 3}, {date: new Date(2012, 10, 08), value: 3}, {date: new Date(2012, 10, 09), value: 11}, {date: new Date(2012, 10, 10), value: 1}, {date: new Date(2012, 10, 13), value: 2}];
}
function createStockChart1() {
	chart1 = new AmCharts.AmStockChart();
	chart1.pathToImages = "http://www.amcharts.com/lib/images/";

	// DATASETS //////////////////////////////////////////
	var dataSet = new AmCharts.DataSet();
	dataSet.color = "#b0de09";
	dataSet.fieldMappings = [{
		fromField: "value",
		toField: "value"},
	/*{
		fromField: "volume",
		toField: "volume"}*/];
	dataSet.dataProvider = chartData1;
	dataSet.categoryField = "date";

	// set data sets to the chart
	chart1.dataSets = [dataSet];

	// PANELS ///////////////////////////////////////////                                                  
	// first stock panel
	var stockPanel1 = new AmCharts.StockPanel();
	stockPanel1.showCategoryAxis = false;
	stockPanel1.title = "Value";
	stockPanel1.percentHeight = 70;

	// graph of first stock panel
	var graph1 = new AmCharts.StockGraph();
	graph1.valueField = "value";
	stockPanel1.addStockGraph(graph1);

	// create stock legend                
	var stockLegend1 = new AmCharts.StockLegend();
	stockLegend1.valueTextRegular = " ";
	stockLegend1.markerType = "none";
	stockPanel1.stockLegend = stockLegend1;

	/*
	// second stock panel
	var stockPanel2 = new AmCharts.StockPanel();
	stockPanel2.title = "Volume";
	stockPanel2.percentHeight = 30;
	var graph2 = new AmCharts.StockGraph();
	graph2.valueField = "volume";
	graph2.type = "column";
	graph2.fillAlphas = 1;
	stockPanel2.addStockGraph(graph2);*/

	// create stock legend
	/*
	var stockLegend2 = new AmCharts.StockLegend();
	stockLegend2.valueTextRegular = " ";
	stockLegend2.markerType = "none";
	stockPanel2.stockLegend = stockLegend2;*/

	// set panels to the chart
	chart1.panels = [stockPanel1];


	// OTHER SETTINGS ////////////////////////////////////
	var scrollbarSettings = new AmCharts.ChartScrollbarSettings();
	scrollbarSettings.graph = graph1;
	scrollbarSettings.updateOnReleaseOnly = true;
	chart1.chartScrollbarSettings = scrollbarSettings;

	var cursorSettings = new AmCharts.ChartCursorSettings();
	cursorSettings.valueBalloonsEnabled = true;
	chart1.chartCursorSettings = cursorSettings;


	// PERIOD SELECTOR ///////////////////////////////////
	var periodSelector = new AmCharts.PeriodSelector();
	periodSelector.periods = [{
		period: "DD",
		count: 10,
		label: "10 days"},
	{
		period: "MM",
		count: 1,
		label: "1 month"},
	{
		period: "YYYY",
		count: 1,
		label: "1 year"},
	{
		period: "YTD",
		label: "YTD"},
	{
		period: "MAX",
		label: "MAX"}];
	chart1.periodSelector = periodSelector;


	var panelsSettings = new AmCharts.PanelsSettings();
	panelsSettings.usePrefixes = true;
	chart1.panelsSettings = panelsSettings;


	// EVENTS
	var e0 = {
		date: new Date(2010, 8, 19),
		type: "sign",
		backgroundColor: "#85CDE6",
		graph: graph1,
		text: "S",
		description: "This is description of an event"
	};
	var e1 = {
		date: new Date(2010, 10, 19),
		type: "flag",
		backgroundColor: "#FFFFFF",
		backgroundAlpha: 0.5,
		graph: graph1,
		text: "F",
		description: "Some longer\ntext can also\n be added"
	};
	var e2 = {
		date: new Date(2010, 11, 10),
		showOnAxis: true,
		backgroundColor: "#85CDE6",
		type: "pin",
		text: "X",
		graph: graph1,
		description: "This is description of an event"
	};
	var e3 = {
		date: new Date(2010, 11, 26),
		showOnAxis: true,
		backgroundColor: "#85CDE6",
		type: "pin",
		text: "Z",
		graph: graph1,
		description: "This is description of an event"
	};
	var e4 = {
		date: new Date(2011, 0, 3),
		type: "sign",
		backgroundColor: "#85CDE6",
		graph: graph1,
		text: "U",
		description: "This is description of an event"
	};
	var e5 = {
		date: new Date(2011, 1, 6),
		type: "sign",
		graph: graph1,
		text: "D",
		description: "This is description of an event"
	};
	var e6 = {
		date: new Date(2011, 3, 5),
		type: "sign",
		graph: graph1,
		text: "L",
		description: "This is description of an event"
	};
	var e7 = {
		date: new Date(2011, 3, 5),
		type: "sign",
		graph: graph1,
		text: "R",
		description: "This is description of an event"
	};
	var e8 = {
		date: new Date(2011, 5, 15),
		type: "arrowUp",
		backgroundColor: "#00CC00",
		graph: graph1,
		description: "This is description of an event"
	};
	var e9 = {
		date: new Date(2011, 6, 25),
		type: "arrowDown",
		backgroundColor: "#CC0000",
		graph: graph1,
		description: "This is description of an event"
	};
	var e10 = {
		date: new Date(2011, 8, 1),
		type: "text",
		graph: graph1,
		text: "Longer text can\nalso be displayed",
		description: "This is description of an event"
	};

	dataSet.stockEvents = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10];

	chart1.write('chartdiv');
}
var chartData2 = [];
var chart2;
function generateChartData2(){
	var firstDate = new Date();
    firstDate.setDate(firstDate.getDate() - 50);

    for (var i = 0; i < 50; i++) {
        var newDate = new Date(firstDate);
        newDate.setDate(newDate.getDate() + i);

        var visits = Math.round(Math.random() * 40) + 100;
        var hits = Math.round(Math.random() * 80) + 500;
        var views = Math.round(Math.random() * 6000);

        chartData2.push({
            date: newDate,
            visits: visits,
            hits: hits,
            views: views
        });
    }
}
function createStockChart2(){
	// SERIAL CHART    
    chart2 = new AmCharts.AmSerialChart();
    chart2.marginTop = 0;
    chart2.autoMarginOffset = 5;
    chart2.pathToImages = "http://www.amcharts.com/lib/images/";
    chart2.zoomOutButton = {
        backgroundColor: '#000000',
        backgroundAlpha: 0.15
    };
    chart2.dataProvider = chartData2;
    chart2.categoryField = "date";

    // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
    chart2.addListener("dataUpdated", zoomChart);

    // AXES
    // category                
    var categoryAxis = chart2.categoryAxis;
    categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
    categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
    categoryAxis.dashLength = 2;
    categoryAxis.gridAlpha = 0.15;
    categoryAxis.axisColor = "#DADADA";

    // first value axis (on the left)
    var valueAxis1 = new AmCharts.ValueAxis();
    valueAxis1.axisColor = "#FF6600";
    valueAxis1.axisThickness = 2;
    valueAxis1.gridAlpha = 0;
    chart2.addValueAxis(valueAxis1);

    // second value axis (on the right) 
    var valueAxis2 = new AmCharts.ValueAxis();
    valueAxis2.position = "right"; // this line makes the axis to appear on the right
    valueAxis2.axisColor = "#FCD202";
    valueAxis2.gridAlpha = 0;
    valueAxis2.axisThickness = 2;
    chart2.addValueAxis(valueAxis2);

    // third value axis (on the left, detached)
    valueAxis3 = new AmCharts.ValueAxis();
    valueAxis3.offset = 50; // this line makes the axis to appear detached from plot area
    valueAxis3.gridAlpha = 0;
    valueAxis3.axisColor = "#B0DE09";
    valueAxis3.axisThickness = 2;
    chart2.addValueAxis(valueAxis3);

    // GRAPHS
    // first graph
    var graph1 = new AmCharts.AmGraph();
    graph1.valueAxis = valueAxis1; // we have to indicate which value axis should be used
    graph1.title = "转发微博数";
    graph1.valueField = "visits";
    graph1.bullet = "round";
    graph1.hideBulletsCount = 30;
    chart2.addGraph(graph1);

    // second graph                
    var graph2 = new AmCharts.AmGraph();
    graph2.valueAxis = valueAxis2; // we have to indicate which value axis should be used
    graph2.title = "原创微博数";
    graph2.valueField = "hits";
    graph2.bullet = "square";
    graph2.hideBulletsCount = 30;
    chart2.addGraph(graph2);

    // third graph
    var graph3 = new AmCharts.AmGraph();
    graph3.valueAxis = valueAxis3; // we have to indicate which value axis should be used
    graph3.valueField = "views";
    graph3.title = "green line";
    graph3.bullet = "triangleUp";
    graph3.hideBulletsCount = 30;
    chart2.addGraph(graph3);

    // CURSOR
    var chartCursor = new AmCharts.ChartCursor();
    chartCursor.cursorPosition = "mouse";
    chart2.addChartCursor(chartCursor);

    // SCROLLBAR
    var chartScrollbar = new AmCharts.ChartScrollbar();
    chart2.addChartScrollbar(chartScrollbar);

    // LEGEND
    var legend = new AmCharts.AmLegend();
    legend.marginLeft = 110;
    chart2.addLegend(legend);

    // WRITE
    chart2.write("chartdiv2");
}

// this method is called when chart is first inited as we listen for "dataUpdated" event
function zoomChart() {
    // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
    chart2.zoomToIndexes(10, 20);
}

var oopts = {textHeight: 25,maxSpeed: 0.03,decel: 0.98,depth: 0.92,outlineColour: '#f6f',outlineThickness: 3,pulsateTo: 0.2,pulsateTime: 0.5,wheelZoom: false,textColour:'#00f',shadow:'#ccf',minBrightness:0.2,shadowBlur:3,weight:true,weightMode:'both'};
function redraw_tagcanvas() {
	if(!$('#myCanvas').tagcanvas(oopts,'tags_div')) {
		$('#myCanvas').hide();
	}
}


var chart3;
var legend3;

var chartData = [
				 /*{
    sex: "男",
    value: 487},
{
    sex: "女",
    value: 95},*/
	{
		sex:"桌面客户端",
		value:19},{
		sex:"浏览器",
		value:378},{
		sex:"移动客户端",
		value:183},
];

function createPieChart(){
	// PIE CHART
    chart3 = new AmCharts.AmPieChart();
    chart3.dataProvider = chartData;
    chart3.titleField = "sex";
    chart3.valueField = "value";
    chart3.outlineColor = "#FFFFFF";
    chart3.outlineAlpha = 0.8;
    chart3.outlineThickness = 2;
    // this makes the chart 3D
    chart3.depth3D = 15;
    chart3.angle = 30;

    // WRITE
    chart3.write("chartdiv3");
}

$(function(){
	// masonry plugin call
	$('#container').masonry({itemSelector : '.item',});
	
	redraw_tagcanvas();

	//injecting arrow points
	function Arrow_Points(){
		var s = $("#container").find(".item");
		$.each(s,function(i,obj){
			var posLeft = $(obj).css("left");
			if(posLeft == "0px"){
				html = " <span class='rightCorner' ></span>";
				$(obj).prepend(html);
			}
			else {
				html = " <span class='leftCorner' ></span>";
				$(obj).prepend(html);
			}
		});
	}
	Arrow_Points();
	
	//generate chart for "关注度分析"
	generateChartData1();
	createStockChart1();
		
	//generate chart for 
	generateChartData2();
	createStockChart2();
	
	//generate sex pie chart
	createPieChart();
});







