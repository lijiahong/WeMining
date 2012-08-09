function autofulfill(word){
    document.getElementById("search_box").value = word;
}

$(document).ready(function(){
    $("#search_box").tagSuggest({
	url: '/api/topic/suggest.json',
	delay: 250
    });
    $("#search_button").click(function() {
	var _topic = $("#search_box")[0].value;
	if(_topic == " " || _topic == ''){
	    $('#warning').show();
	    return;
	}
	else{
	    $('#warning').hide();
	    window.location.href="/topicweibo/analysis?topic=" + _topic;
	}
    });
    $("#follow_pic").click(function() {
	$('#information').html('')
	var _topic = $("#search_box")[0].value;
	if(_topic == " " || _topic == ''){
	    $('#warning').show();
	    return;
	}
	else{
	    $('#warning').hide();
	    $.ajax({
		url: '/topicweibo/followtrends?topic='+_topic,
		dataType: 'json',
		success: function(d) {
		    console.log(d.status);
		    if(d.status == 'is followed')
			$('#information').html('该话题您已经关注过了.')
		    else if(d.status == 'follow ok')
			$('#information').html('关注成功.')
		    else if(d.status == 'need login')
			$('#information').html('请登录新浪微博.')
		    else
			$('#information').html('关注失败.')
		}
	    });	    
	}
    });
    $.ajax({
	url: '/api/topic/now.json',
	dataType: 'json',
	success: function(d) {
	    for(type in d ){
		data = d[type];
		for(var i=0;i<data.length;i+=1){
                    data[i][0] = data[i][0].replace(/\s/g,"");
		    $('#hotTopics_'+type).append("<li><a href='#' class='tag" + data[i][2] + "' title='选择话题' onclick=autofulfill('" + data[i][0] + "')>" + data[i][0] + "</a></li>" );}
	    };
	}
    });
});
