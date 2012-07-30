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
});
