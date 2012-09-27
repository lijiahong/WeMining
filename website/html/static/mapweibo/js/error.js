var status = (getUrlParam("status")==null)?"other":getUrlParam("status");
var page = (getUrlParam("page")==null)?"mapweibo":getUrlParam("page");
function getUrlParam(name) { 
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
	var r = window.location.search.substr(1).match(reg); 
	if (r != null){ 
		return decodeURI(r[2]); 
	}
	return null; 
} 
function goTo(){
	if(page == "mapweibo"){
		window.location.href="/weiming/mapweibo";
	}
	else if(page == "sentimentview"){
		window.location.href="/weiming/mapweibo/sentimentview";
	}
	else if(page == "mapview"){
		window.location.href="/weiming/mapweibo/mapview";
	}
}
function initial_DOM(){
	if(page == "mapweibo"){
		$("#page").empty();
		$("#page").append("<span class=\"W_spetxt\" id=\"reload_num_span\">10</span>秒之后页面自动跳转至<a href=\"/weiming/mapweibo\">mapWeibo首页</a>，您还可以重新输入<strong>筛选条件</strong>包括：");
	}
	else if(page == "sentimentview"){
		$("#page").empty();
		$("#page").append("<span class=\"W_spetxt\" id=\"reload_num_span\">10</span>秒之后页面自动跳转至<a href=\"/weiming/mapweibo/sentimentview\">情绪示例页面</a>，您还可以重新输入<strong>筛选条件</strong>包括：");
	}
	else if(page == "mapview"){
		$("#page").empty();
		$("#page").append("<span class=\"W_spetxt\" id=\"reload_num_span\">10</span>秒之后页面自动跳转至<a href=\"/weiming/mapweibo/mapview\">传播示例页面</a>，您还可以重新输入<strong>筛选条件</strong>包括：");
	}
	if(status == "sentiment_limit_illegal"){
		$("#reason").append("<dd>输入的微博数量上限过少，或是输入的时间片段数不在0到100之间</dd>");
	}
	else if(status == "sentiment_count_little"){
		$("#reason").append("<dd>话题的微博总数过少，需重新选择话题分析</dd>");
	}
	else if(status == "sentimentview_broken_down"){
		$("#reason").append("<dd>话题的微博总数过多，无法分析，需重新选择话题分析</dd>");
	}
	else if(status == "total_number_too_much"){
		$("#reason").append("<dd>话题的微博总数过多，无法分析，需重新选择话题分析</dd>");
	}
	else if(status == "real_number_too_much"){
		$("#reason").append("<dd>分析的微博数量过多或过少，需重新选择话题或改变时间区间分析</dd>");
	}
	else if(status == "mapview_broken_down"){
		$("#reason").append("<dd>话题的微博总数过多，无法分析，需重新选择话题分析</dd>");
	}
	else{
		$("#reason").append("<dd>此话题无法分析，若执意分析，请联系<a href=\"http://weibo.com/linhao199201\">LinHaoBuaa</a></dd>");
	}
}
$(document).ready(function(){
    initial_DOM();
	var box = document.getElementById('reload_num_span');
	var time  = parseInt(box.innerHTML, 10);
	function go() {
		box.innerHTML = time;
		time = time-1;
		
		if(time > 0) {
			setTimeout(go, 1000);
		}
	}
	go();
	setTimeout(goTo,10000);
});