LineClusterer.prototype = new google.maps.OverlayView();
LineClusterer.prototype.onAdd = function() { };
LineClusterer.prototype.onRemove = function() { };
LineClusterer.prototype.draw = function() {};
LineClusterer.prototype.idle = function(){};

var time_out_;
function LineClusterer(map, lines_data){
    this.map = map;
    this.step_sum = 10;
    this.timeout = 250;
    this.lines = []
    for(latlng in lines_data){
	latlngs = latlng.split('-');
	rank = lines_data[latlng].rank;
	repost_count = lines_data[latlng].count;
	release_province_latlng = latlngs[0];
	forward_province_latlng = latlngs[1];
	start_point = new google.maps.LatLng(release_province_latlng.split(' ')[0], release_province_latlng.split(' ')[1]);
	end_point = new google.maps.LatLng(forward_province_latlng.split(' ')[0], forward_province_latlng.split(' ')[1]);
	path = [];
	var step_lat = (end_point.lat()-start_point.lat())/this.step_sum;
	var step_lng = (end_point.lng()-start_point.lng())/this.step_sum;
	for(var y=0;y<this.step_sum;y++){
	    path.push([start_point, new google.maps.LatLng(start_point.lat()+step_lat*(y+1), start_point.lng()+step_lng*(y+1))]);
	}
	path.push([start_point, end_point]);
	this.lines.push({'path': path, 'rank': rank, 'repost_num': repost_count})
    }
    var lines_ = [];
    var x = 0;
    var that = this;
    (function(){
	if(lines_ != []){
	    for(var i=0;i<lines_.length;i++){
		lines_[i].setMap(null);
	    }
	    lines_ = [];
	}
	for(var i=0;i<that.lines.length;i++){
	    var linecolor;
	    var lineweight;
	    lineweight = Math.ceil(that.lines[i].repost_num / 10);
	    switch(that.lines[i].rank){
	    case 1:linecolor = '#99cc99';break;//»Ò
	    case 2:linecolor = 'ffbf00';break;//»Æ
	    case 3:linecolor = 'ff0000';break;//ºì
	    }
	    that.lines[i].polyline = new google.maps.Polyline({  
		map: that.map,
		strokeColor: linecolor,
		strokeOpacity: 1,
		strokeWeight: lineweight,
		path: that.lines[i].path[x]
	    });
	    lines_.push(that.lines[i].polyline);
	}
	x++;
	time_out_ = setTimeout(arguments.callee, that.timeout);
	if(x >= that.step_sum) 
	    clearTimeout(time_out_);
    })();
}

LineClusterer.prototype.clearlines = function(){
    for(var x=0;x<this.lines.length;x++){
	if(time_out_ != undefined){
	    clearTimeout(time_out_);
	}
	this.lines[x].polyline.setMap(null);
    }
}
LineClusterer.prototype.getlines = function(){
    var lines = [];
    for(var i=0;i<this.lines.length;i++){
	lines.push(this.lines[i].polyline);
    }
    return lines;
}



/**
 * Extends a objects prototype by anothers.
 *
 * @param {Object} obj1 The object to be extended.
 * @param {Object} obj2 The object to extend with.
 * @return {Object} The new extended object.
 * @ignore
 */
LineClusterer.prototype.extend = function(obj1, obj2) {
  return (function(object) {
    for (property in object.prototype) {
      this.prototype[property] = object.prototype[property];
    }
    return this;
  }).apply(obj1, [obj2]);
};

// Export Symbols for Closure
// If you are not going to compile with closure then you can remove the
// code below.
window['LineClusterer'] = LineClusterer;
LineClusterer.prototype['extend'] = LineClusterer.prototype.extend;
LineClusterer.prototype['onAdd'] = LineClusterer.prototype.onAdd;
LineClusterer.prototype['onRemove'] = LineClusterer.prototype.onRemove;
LineClusterer.prototype['idle'] = LineClusterer.prototype.idle;
LineClusterer.prototype['draw'] = LineClusterer.prototype.draw;

LineClusterer.prototype['clearline'] = LineClusterer.prototype.clearline;

