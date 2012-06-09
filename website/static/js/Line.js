LineClusterer.prototype = new google.maps.OverlayView();
LineClusterer.prototype.onAdd = function() { };
LineClusterer.prototype.onRemove = function() { };
LineClusterer.prototype.draw = function() {};
LineClusterer.prototype.idle = function(){};

var time_out_;
function LineClusterer(map,line_data){
	this.map_ = map;
	this.lines_ = [];
	for(var x = 0;x < line_data.length;x = x + 1){
	    this.lines_.push({release_province_latlng: line_data[x].release_province_latlng,
						  forward_province_latlng: line_data[x].forward_province_latlng,
						  repostnum_: line_data[x].repost_num,
						  rank_: line_data[x].rank,
						  startLatLng_ : '',
						  endLatLng_ : '',
						  polyline_ : '',
						});
	}
	this.step_sum = 10;
	this.timeout = 250;
		
	for(var x = 0; x < this.lines_.length; x = x + 1){
		this.lines_[x].startLatLng_ = new google.maps.LatLng(this.lines_[x].release_province_latlng.split(' ')[0],this.lines_[x].release_province_latlng.split(' ')[1]);
		this.lines_[x].endLatLng_ = new google.maps.LatLng(this.lines_[x].forward_province_latlng.split(' ')[0],this.lines_[x].forward_province_latlng.split(' ')[1]);
		
		this.lines_[x].path = [];
		
		//var target_total_distance_ = google.maps.geometry.spherical.computeDistanceBetween(this.lines_[x].startLatLng_,this.lines_[x].endLatLng_);
		
		//var target_direction = google.maps.geometry.spherical.computeHeading(this.lines_[x].startLatLng_,this.lines_[x].endLatLng_);
		
		var step_lat = (this.lines_[x].endLatLng_.lat() - this.lines_[x].startLatLng_.lat()) / this.step_sum;
		var step_lng = (this.lines_[x].endLatLng_.lng() - this.lines_[x].startLatLng_.lng()) / this.step_sum;
		
		//var each_step_dis = target_total_distance_/this.step_sum;
		//var dis = each_step_dis;
		
		for(var y = 0;y < this.step_sum;y = y + 1){
			//this.lines_[x].path.push([this.lines_[x].startLatLng_,google.maps.geometry.spherical.computeOffset(this.lines_[x].startLatLng_,dis,target_direction)]);
			this.lines_[x].path.push([this.lines_[x].startLatLng_,new google.maps.LatLng(this.lines_[x].startLatLng_.lat()+step_lat*(y+1), this.lines_[x].startLatLng_.lng()+step_lng*(y+1))]);
			//dis = dis + each_step_dis;
		}
		this.lines_[x].path.push([this.lines_[x].startLatLng_,this.lines_[x].endLatLng_]);
				
	}
	
		var line_ = [];
		var x = 0;
		var that = this;
		(function(){
			if(line_ != []){
				for(var y = 0;y < line_.length;y = y + 1){
					line_[y].setMap(null);
				}
				line_ = [];
			}
			for(var y = 0;y < that.lines_.length;y = y + 1){
				var linecolor;
				var lineweight;
				lineweight = Math.ceil(that.lines_[y].repostnum_ / 10);
				switch(that.lines_[y].rank_){
					case 1:linecolor = '#99cc99';break;//»Ò
					case 2:linecolor = 'ffbf00';break;//»Æ
					case 3:linecolor = 'ff0000';break;//ºì
				}
				that.lines_[y].polyline_ = new google.maps.Polyline({  
					map: that.map_,
					strokeColor: linecolor,
					strokeOpacity: 1,
					strokeWeight: lineweight,
					path: that.lines_[y].path[x]
			   });
				line_.push(that.lines_[y].polyline_);
			}
			x++;
			time_out_ = setTimeout(arguments.callee, that.timeout);
			if(x >= that.step_sum) clearTimeout(time_out_);
		})();
}

LineClusterer.prototype.clearlines = function(){
	for(var x = 0;x < this.lines_.length; x = x + 1){
	   if(time_out_ != undefined){
		   clearTimeout(time_out_);
	   }
	   this.lines_[x].polyline_.setMap(null);
	}
}
LineClusterer.prototype.getlines = function(){
	var lines = [];
	for(var x = 0;x < this.lines_.length; x = x + 1){
	   lines.push(this.lines_[x].polyline_);
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

