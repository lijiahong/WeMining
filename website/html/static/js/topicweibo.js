function autofulfill(word){
    document.getElementById("search_box").value = word;
}

$(document).ready(function(){
    $("#search_button").click(function() {
  	console.log("here");
	var _topic = $("#search_box")[0].value;
	console.log(_topic);
	if(_topic != undefined){
	    window.location.href="/topicweibo/analysis?topic=" + _topic;
	}
    });
    $.ajax({
	url: '/api/topic/now.json',
	dataType: 'json',
	success: function(d) {
	    for(type in d ){
		data = d[type];
		for(var i=0;i<data.length;i+=1){
		    $('#hotTopics_'+type).append('<li><a href="#search_box" class="tag' + data[i][2] + '" title="选择话题" onclick=autofulfill("' + data[i][0] + '")>' + data[i][0] + '</a></li>');}
	    };
	}
    });
});
