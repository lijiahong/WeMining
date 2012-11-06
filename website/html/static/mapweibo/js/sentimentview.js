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
/*
Array.prototype.min = function() {  
	var min = this[0];  
	var len = this.length;  
	for (var i = 1; i < len; i++){  
		if (this[i] < min){  
			min = this[i];  
		}  
	}  
	return min;  
}  
//最大值  
Array.prototype.max = function() {  
	var max = this[0];  
	var len = this.length;  
	for (var i = 1; i < len; i++){  
		if (this[i] > max) {  
			max = this[i];  
		}  
	}  
	return max;  
}  
*/
/*
作者：无涯 2007年3月27日 xrwang@126.com
许可：在保留作者信息的前提下，本文件可以随意修改、传播、使用，但对可能由此造成的损失作者不负担任何责任。
Dictionary类：本类实现了字典功能，所有方法、属性都模仿System..Collection.Generic.Dictionary类
构造函数：
	Dictionary()
属性：
	CompareMode：比较模式，0——二进制   1——文本
	Count：字典中的项目数
	ThrowException：遇到错误时，是否抛出异常
方法：
	Item(key)：获取指定键对应的值
	Keys()：获取键数组
	Values()：获取值数组
	Add(key,value)：将指定的键和值添加到字典中
	BatchAdd(keys,values)：尝试将指定的键和值数组添加到字典中，如果全部添加成功，返回true；否则返回false。
	Clear()：清除字典中的所有项
	ContainsKey(key)：字典中是否包含指定的键
	ContainsValue(value)：字典中是否包含指定的值
	Remove(key)：删除字典中指定的键
	TryGetValue(key,defaultValue)：尝试获取字典中指定键对应的值，如果键不存在，返回默认值
	ToString()：返回字典中所有键和值组成的字符串，格式为“逗号分隔的键列表  分号  逗号分隔的值列表”
*/

function Dictionary()
{
    var me=this;            //将this指针保存到变量me中
    this.CompareMode=1;        //比较关键字是否相等的模式，0——二进制；1——文本 
    this.Count=0;            //字典中的项目数
    this.arrKeys=new Array();    //关键字数组
    this.arrValues=new Array();    //值数组
    this.ThrowException=true;    //遇到错误时，是否用throw语句抛出异常
    this.Item=function(key)        //Item方法，获取指定键对应的值。如果键不存在，引发异常
    {
        var idx=GetElementIndexInArray(me.arrKeys,key);
        if(idx!=-1)
        {
            return me.arrValues[idx];
        }
        else
        {
            if(me.ThrowException)
                throw "在获取键对应的值时发生错误，键不存在。";
        }
    }
    this.Keys=function()        //获取包含所有键的数组
    {
        return me.arrKeys;
    }
    this.Values=function()        //获取包含所有值的数组
    {
        return me.arrValues;
    }
    this.Add=function(key,value)    //将指定的键和值添加到字典中
    {
        if(CheckKey(key))
        {
            me.arrKeys[me.Count]=key;
            me.arrValues[me.Count]=value;
            me.Count++;
        }
        else
        {
            if(me.ThrowException)
                throw "在将键和值添加到字典时发生错误，可能是键无效或者键已经存在。";
        }
    }
    this.BatchAdd=function(keys,values)        //批量增加键和值数组项，如果成功，增加所有的项，返回true；否则，不增加任何项，返回false。
    {
        var bSuccessed=false;
        if(keys!=null && keys!=undefined && values!=null && values!=undefined)
        {
            if(keys.length==values.length && keys.length>0)    //键和值数组的元素数目必须相同
            {
                var allKeys=me.arrKeys.concat(keys);    //组合字典中原有的键和新键到一个新数组
                if(!IsArrayElementRepeat(allKeys))    //检验新数组是否存在重复的键
                {
                    me.arrKeys=allKeys;
                    me.arrValues=me.arrValues.concat(values);
                    me.Count=me.arrKeys.length;
                    bSuccessed=true;
                }
            }
        }
        return bSuccessed;
    }
    this.Clear=function()            //清除字典中的所有键和值
    {
        if(me.Count!=0)
        {
            me.arrKeys.splice(0,me.Count);
            me.arrValues.splice(0,me.Count);
            me.Count=0;
        }
    }
    this.ContainsKey=function(key)    //确定字典中是否包含指定的键
    {
        return GetElementIndexInArray(me.arrKeys,key)!=-1;
    }
    this.ContainsValue=function(value)    //确定字典中是否包含指定的值
    {
        return GetElementIndexInArray(me.arrValues,value)!=-1;
    }
    this.Remove=function(key)        //从字典中移除指定键的值
    {
        var idx=GetElementIndexInArray(me.arrKeys,key);
        if(idx!=-1)
        {
            me.arrKeys.splice(idx,1);
            me.arrValues.splice(idx,1);
            me.Count--;
            return true;
        }
        else
            return false;
    }
    this.TryGetValue=function(key,defaultValue)    //尝试从字典中获取指定键对应的值，如果指定键不存在，返回默认值defaultValue
    {
        var idx=GetElementIndexInArray(me.arrKeys,key);
        if(idx!=-1)
        {
            return me.arrValues[idx];
        }
        else
            return defaultValue;
    }
    this.ToString=function()        //返回字典的字符串值，排列为： 逗号分隔的键列表  分号  逗号分隔的值列表
    {
        if(me.Count==0)
            return "";
        else
            return me.arrKeys.toString() + ";" + me.arrValues.toString();
    }
    function CheckKey(key)            //检查key是否合格，是否与已有的键重复
    {
        if(key==null || key==undefined || key=="" || key==NaN)
            return false;
        return !me.ContainsKey(key);
    }
    function GetElementIndexInArray(arr,e)    //得到指定元素在数组中的索引，如果元素存在于数组中，返回所处的索引；否则返回-1。
    {
        var idx=-1;    //得到的索引
        var i;        //用于循环的变量
        if(!(arr==null || arr==undefined || typeof(arr)!="object"))
        {
            try
            {
                for(i=0;i<arr.length;i++)
                {
                    var bEqual;
                    if(me.CompareMode==0)
                        bEqual=(arr[i]===e);    //二进制比较
                    else
                        bEqual=(arr[i]==e);        //文本比较
                    if(bEqual)
                    {
                        idx=i;
                        break;
                    }
                }
            }
            catch(err)
            {
            }
        }
        return idx;
    }
    function IsArrayElementRepeat(arr)    //判断一个数组中的元素是否存在重复的情况，如果存在重复的元素，返回true，否则返回false。
    {
        var bRepeat=false;
        if(arr!=null && arr!=undefined && typeof(arr)=="object")
        {
            var i;
            for(i=0;i<arr.length-1;i++)
            {
                var bEqual;
                if(me.CompareMode==0)
                    bEqual=(arr[i]===arr[i+1]);    //二进制比较
                else
                    bEqual=(arr[i]==arr[i+1]);        //文本比较
                if(bEqual)
                {
                    bRepeat=true;
                    break;
                }
            }
        }
        return bRepeat;
    }
}


var map;
var heatmap1;                //快乐热图层
var heatmap2;				 //生气热图层
var heatmap3;				 //悲伤热图层
var heatmap_type = 0;        //当前图层类型
var stoped=true;
var distinct_time = [];     //数据时间分割点数组
var most_province;			//最情绪数据

var raw_data;				//存储从服务器返回的数据
var markers;


function getUrlParam(name) { 
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); 
	var r = window.location.search.substr(1).match(reg); 
	if (r != null){ 
		return decodeURI(r[2]); 
	}
	return null; 
} 


function getNowTime(){
	var now = new Date();
	var year=now.getFullYear();  
    var month=now.getMonth()+1;  
    var day=now.getDate();
	var d = year + "-" + month + "-" + day;
	//console.log(d);
	return d;
}

var sentiment = {
	getPresentTopic: (getUrlParam('topic')==null)?'钓鱼岛':getUrlParam('topic'),
	getPresentCollection: (getUrlParam('topic')==null)?'user_statuses':getUrlParam('collection'),
	step_sum : (getUrlParam('timeInterval')==null)?25:getUrlParam('timeInterval'),       //规定slider的步数总和
	limit : (getUrlParam('limit')==null)?40000:getUrlParam('limit'),
	count : 0,
	//starttime: (getUrlParam('starttime')==null)?'2012-01-01':getUrlParam('starttime'), 
	//endtime: (getUrlParam('endtime')==null)?getNowTime():getUrlParam('endtime'),
	now_step : 0,

	inter_slider : null,
	interval_time : 5000,
    initialOptions : {
        zoom : 4,
		minZoom : 3,
        center: new google.maps.LatLng(35.563611,103.36388611),
        mapTypeId: google.maps.MapTypeId.ROADMAP,//SATELLITE,
        navigationControlOptions : {
            style: google.maps.NavigationControlStyle.ZOOM_PAN,
            position: google.maps.ControlPosition.TOP_LEFT
        },
        mapTypeControlOptions : {
            style : google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
		overviewMapControl : true,
		overviewMapControlOptions : {
			opened : true,
			position: google.maps.ControlPosition.BOTTOM_LEFT
		},
		panControl : true,
		panControlOptions : {
			position : google.maps.ControlPosition.TOP_LEFT,
		},
		rotateControl : true,
		rotateControlOptions : {
			position: google.maps.ControlPosition.TOP_CENTER, 
		}
    },
    reset : function () { 
        map.panTo(sentiment.initialOptions.center);
        map.setZoom(sentiment.initialOptions.zoom);
    },    
    markerIcons: {
		happy : {
			'1' : '/static/mapweibo/images/emoticon/we_Happy_8x8.png',
			'2' : '/static/mapweibo/images/emoticon/we_Happy_16x16.png',
			'3' : '/static/mapweibo/images/emoticon/we_Happy_24x24.png',
			'4' : '/static/mapweibo/images/emoticon/we_Happy_32x32.png'
		},
		angry : {
			'1' : '/static/mapweibo/images/emoticon/we_Negative_8x8a.png',
			'2' : '/static/mapweibo/images/emoticon/we_Negative_16x16a.png',
			'3' : '/static/mapweibo/images/emoticon/we_Negative_24x24a.png',
			'4' : '/static/mapweibo/images/emoticon/we_Negative_32x32a.png'
		},
		sad : {
			'1': '/static/mapweibo/images/emoticon/we_Sad_8x8.png',
			'2': '/static/mapweibo/images/emoticon/we_Sad_16x16.png',
			'3': '/static/mapweibo/images/emoticon/we_Sad_24x24.png',
			'4': '/static/mapweibo/images/emoticon/we_Sad_32x32.png'
		},
	},
	markersByCategory : {
		happy : [],
		angry: [],
		sad : []
	},
	clearMarkersByCategory : function (category) {
		sentiment.markersByCategory['happy'] = [];
		sentiment.markersByCategory['angry'] = [];
		sentiment.markersByCategory['sad'] = [];
	},
    showMarkersByCategory : function (category) {
        for (var k=0; k<sentiment.markersByCategory[category].length; k+=1) {
			var thisMarker = sentiment.markersByCategory[category][k];
            sentiment.markersByCategory[category][k].setVisible(true);
        }
    },
    hideMarkersByCategory : function (category) {
        for (var i=0; i<sentiment.markersByCategory[category].length; i+=1) {
            var thisMarker = sentiment.markersByCategory[category][i];
            thisMarker.setVisible(false);
     
        }
    },
	//省份对应顺序：北京，上海，天津，重庆，河北，河南，湖北，湖南，江苏，江西，辽宁，吉林，黑龙江，陕西，山西，山东，四川，青海，安徽，海南，广东，贵州，浙江，福建，台湾，甘肃，云南，西藏，宁夏，广西，新疆，内蒙古，香港，澳门
	province_latlngs : ["39.904214 116.407413","31.230393 121.473704","39.084158 117.200983","29.56301 106.551557","38.037057 114.468665","34.76819 113.687228","30.545861 114.341921","28.112444 112.98381","32.061707 118.763232","28.674424 115.909175","41.835441 123.42944","43.837883 126.549572","45.74217 126.662507","34.265472 108.954239","37.873376 112.562569","36.668627 117.020411","30.651652 104.075931","36.620901 101.780199","31.861184 117.284923","20.017378 110.349229","23.132191 113.266531","26.598026 106.707116","30.26586 120.153676","26.099933 119.296506","23.69781 120.960515","36.059421 103.826308","25.045359 102.709812","29.647951 91.117006","38.471318 106.258754","22.815478 108.327546","43.793028 87.627812","40.817498 111.765618","22.396428 114.109497","22.198745 113.543873"],
			
	index_province : {1:"北京",2:"上海",3:"天津",4:"重庆",5:"河北",6:"河南",7:"湖北",8:"湖南",9:"江苏",10:"江西",11:"辽宁",12:"吉林",13:"黑龙江",14:"陕西",15:"山西",16:"山东",17:"四川",18:"青海",19:"安徽",20:"海南",21:"广东",22:"贵州",23:"浙江",24:"福建",25:"台湾",26:"甘肃",27:"云南",28:"西藏",29:"宁夏",30:"广西",31:"新疆",32:"内蒙古",33:"香港",34:"澳门"},
	
	
};

var DOM = {
	ui : function(){
		return{
			init : function () {
				map = new google.maps.Map(document.getElementById('map_canvas'), sentiment.initialOptions);
							
				$('#slider').slider({
									   min: 0,
									   step: 1,
									 });
				$('#play_pause1').button({icons: {primary: "ui-icon-play"},text: false});
				$('#play_pause2').button({icons: {primary: "ui-icon-pause"},text: false});
				$('#play_pause3').button({icons: {primary: "ui-icon-bullet"},text: false});
				if(getUrlParam("topic")!=null && getUrlParam("limit")!=null && getUrlParam("timeinterval")!=null){
					$("#keywords").empty();
					var k_html = "<p>输入<strong>筛选条件</strong>以便开始<strong>新</strong>的分析:</p><div id=\"s_keyword\">               <strong>关键词:</strong><input type=\"text\" name=\"topic\" placeholder=\"请输入关键词...\" value=\"" + sentiment.getPresentTopic + "\" />           </div><div id=\"limit\"><strong>微博数量上限:</strong><input type=\"text\" name=\"limit\" id=\"absolutelimit\" value=\"" + sentiment.limit + "\" style=\"width:100px;\" placeholder=\"请输入绝对数...\" onkeypress=\"check();\" />条 &nbsp;<input type=\"text\" id=\"relativelimit\" placeholder=\"请输入百分数...\" onkeypress=\"check();\" value=\"\" style=\"width:100px;\"/>%&nbsp;<input type=\"label\" id=\"count\" value=\"微博总数\" readonly=\"readonly\"/></div><div id=\"timeinterval\"><strong>时间片段数:</strong><input type=\"text\" name=\"timeinterval\" value=\"" + sentiment.step_sum + "\" />  </div><button id=\"submit\" style=\"margin-left:15px;\">分析</button>";
					$("#keywords").append(k_html);
				}
				
				var topic = sentiment.getPresentTopic;

			
				$("#select_timeInterval").jQselectable({
							style: "simple",
							set: "fadeIn",
							out: "fadeOut",
							//height: 300,
							//width:168,
							opacity: .9,
							callback: function(){
								if($(this).val().length>0){ 	 
								}
							}
				});
				$('#starttime').datepicker({
					changeMonth: true,
					changeYear: true,
					dateFormat: "yy-mm-dd",
					
				});;
				$('#endtime').datepicker({
					changeMonth: true,
					changeYear: true,
					dateFormat: "yy-mm-dd",
					
				});;
						
			}
		}
	}(),
	nationViewButton : function () {
        var htmlElement = '<p id="back-to-nation-view" class="hidden"><span>返回全景模式</span></p>';
        var $element;
        return {
            init : function () {
				$element = $('#mapContainer').append(htmlElement).find('#back-to-nation-view');
                $element.bind('click', function () {
                    sentiment.reset();
                });
				//$element.addClass('hidden');
				$element.removeClass('hidden');
            },
            hide : function () {
                $element.addClass('hidden');
            },
            show : function () {
                $element.removeClass('hidden');
            }
        };
    }(),
	
    init : function () {
	    DOM.nationViewButton.init();
		DOM.ui.init();
		
		$('#console #helpers li#all').addClass('active');
		
		
        $('#console #helpers li#all').bind('click', function () {
			  if(stoped == true){
				var $liAll = $(this);
				if ( !$liAll.hasClass('active') ) {
					$('#console #categories li:.active').each(function () {
						$(this).removeClass('active');
					});
					$liAll.addClass('active');
					heatmap_type = 0;
					if(sentiment.now_step != 0){
						change_map_display();
					}
				}
			  }
        });
		/*
          $('#console #helpers li#all').bind('click', function () {
			  if(stoped == true){
				var $liAll = $(this);
				if ( !$liAll.hasClass('active') ) {
					$('#console #categories li:not(.active)').each(function () {
						sentiment.showMarkersByCategory( $(this).addClass('active').attr('id') );
					});
					$liAll.addClass('active');
					$('#slider').slider("option", "disabled", false);
					$('#play_pause1').button("option", "disabled", false);
					$('#play_pause2').button("option", "disabled", false);
					$('#play_pause3').button("option", "disabled", false);
				}
			  }
        });*/

        $('#console #categories li').bind('click', function () {
		   if(stoped == true){
            var $li = $(this);
            var $liAll = $('#console #helpers li#all');
			if($li.attr('id') == 'happy'){
				heatmap_type = 3;
			}else if($li.attr('id') == 'angry'){
				heatmap_type = 2;
			}else{
				heatmap_type = 1;
			}
			$li.addClass('active');
			$li.siblings('li.active').removeClass('active');
			if ( $liAll.hasClass('active') ) {
				$liAll.removeClass('active');
			}
			if(sentiment.now_step != 0){
				change_map_display();
			}
			/*
            if ( $liAll.hasClass('active') ) {
                $li.siblings('li').each(function () {
                    sentiment.hideMarkersByCategory( $(this).removeClass('active').attr('id') );
                });
                $liAll.removeClass('active');
				$('#slider').slider("option", "disabled", true);
				$('#play_pause1').button("option", "disabled", true);
				$('#play_pause2').button("option", "disabled", true);
				$('#play_pause3').button("option", "disabled", true);
            } else if ( !$li.hasClass('active') ) {
                sentiment.hideMarkersByCategory( $li.siblings('li.active').removeClass('active').attr('id') );
                sentiment.showMarkersByCategory( $li.addClass('active').attr('id') );
				$('#slider').slider("option", "disabled", true);
				$('#play_pause1').button("option", "disabled", true);
				$('#play_pause2').button("option", "disabled", true);
				$('#play_pause3').button("option", "disabled", true);
            }*/
		   }
        });

    }
};

function dataHandle(){
	  //var most_province_data = handle_data_list[1];
	 /*
	  *数据处理
	  */
	  
	  function getUnique(someArray){           //得到一个元素互异的数组
		   tempArray=someArray.slice(0);//复制数组到临时数组
		   for(var i=0;i<tempArray.length;i++){
				 for(var j=i+1;j<tempArray.length;){
					 if(tempArray[j]==tempArray[i]){
						 //后面的元素若和待比较的相同，则删除并计数；
						 //删除后，后面的元素会自动提前，所以指针j不移动
							tempArray.splice(j,1);
					  }
					 else{
							j = j + 1;
					  }					  
						//不同，则指针移动				 
				  }
		   }
		   return tempArray;
	  }	 
			
	  var time_array=[];
				
	  for(var x = 0;x < raw_data.length;x = x + 1){
		  time_array.push(raw_data[x].ts);
		  //console.log(raw_data[x].ts);
		  //console.log(x);
		  
	  } 
	 
	  var primary_distinct_time = getUnique(time_array);//互异的时间数组，且从小到大排序
	  var each_step_index = primary_distinct_time.length / sentiment.step_sum;
	  //console.log(each_step_index);
	  //console.log(primary_distinct_time.length);						  
	  var index = 0;                                    //index是时间分割点索引
	  //获得时间分割点数组distinct_time
	  while(true){
		  if(index < primary_distinct_time.length-1){
			  /*if(index <= 8){
				  distinct_time.push(primary_distinct_time[4]);
				  index = 9;
			  }
			  else{*/
			  var d = primary_distinct_time[Math.round(index)];
		      var str = new Date(d*1000).format('yyyy-MM-dd hh:mm:ss');
			  //console.log(Math.round(index) + ":" + str);
			  distinct_time.push(d);
			  
			  index = index + each_step_index;
			 
		  }
		  else{
			   var d = primary_distinct_time[primary_distinct_time.length-1]
			   var str = new Date(d*1000).format('yyyy-MM-dd hh:mm:ss');
			   //console.log(primary_distinct_time.length-1 + ":" + str);
			  distinct_time.push(d);
			  break;
		  }
	  }
	  //console.log(new Date(distinct_time[0]*1000).format('yyyy-MM-dd hh:mm:ss'));
	  //console.log(distinct_time);
	  sentiment.step_sum = distinct_time.length;		
	  //console.log(sentiment.step_sum);
	  $( "#slider" ).slider( "option", "max", sentiment.step_sum+2);
		  
}

function clearMarkers(){
	  if(markers != undefined && markers != []){
			  for(var m = 0;m < markers.length;m = m + 1){
				  markers[m].setMap(null);
			  }
	  }
	  markers = [];
}
function clearHeatmap(){
	  if(heatmap1 != null){
		  heatmap1.setMap(null);
	  }
	  if(heatmap2 != null){
		  heatmap2.setMap(null);
	  }
	  if(heatmap3 != null){
		  heatmap3.setMap(null);
	  }
}

function change_map_display(){
	
		  clearHeatmap();
		  var arr;
		  var lat;
		  var lng;
		  var count;
		  var dataset = [];
		  var raw = raw_data[sentiment.now_step-1];
		  var raw_detail_province = raw.detail_province;
		  var raw_province_level = raw.province_level;
		  
		  for(var x = 0;x < 33;x = x + 1){
			  console.log(raw_detail_province[x]);
			  //console.log(raw_detail_province[x][1]);
			  arr = raw_detail_province[x][0].split(" ");
			  lat = arr[0];
			  lng = arr[1];
			  count = raw_detail_province[x][1][0];
			  //console.log(count);
			  if(count != 0){
				  dataset.push({location:new google.maps.LatLng(lat,lng),weight:count});
			  }
		  }
		  //console.log(dataset);
		  heatmap1 = new google.maps.visualization.HeatmapLayer({
			  data: dataset,
			  dissipating:true,
			  opacity:0.5,
			  //maxIntensity:max_gradient1,
			  //radius:10,
//gradient:["green"]//["black","silver","gray","white","maroon","red","purple","fuchsia","green","lime","olive","yellow","navy","blue","teal","aqua"]
		  });
		  dataset = [];
		  for(var x = 0;x < raw_detail_province.length;x = x + 1){
			  arr = raw_detail_province[x][0].split(" ");
			  lat = arr[0];
			  lng = arr[1];
			  count = raw_detail_province[x][1][1];
			  if(count != 0){
				  dataset.push({location:new google.maps.LatLng(lat,lng),weight:count});
			  }
		  }
		  heatmap2 = new google.maps.visualization.HeatmapLayer({
			  data: dataset,
			  dissipating:true,
			  opacity:0.5,
			  //maxIntensity:max_gradient1,
			  //radius:10
//gradient:["green"]//["black","silver","gray","white","maroon","red","purple","fuchsia","green","lime","olive","yellow","navy","blue","teal","aqua"]
		  });
		  dataset = [];
		  for(var x = 0;x < raw_detail_province.length;x = x + 1){
			  arr = raw_detail_province[x][0].split(" ");
			  lat = arr[0];
			  lng = arr[1];
			  count = raw_detail_province[x][1][2];
			  if(count != 0){
				  dataset.push({location:new google.maps.LatLng(lat,lng),weight:count});
			  }
		  }
		  heatmap3 = new google.maps.visualization.HeatmapLayer({
			  data: dataset,
			  dissipating:true,
			  opacity:0.5,
			  //maxIntensity:max_gradient1,
			  //radius:10
//gradient:["green"]//["black","silver","gray","white","maroon","red","purple","fuchsia","green","lime","olive","yellow","navy","blue","teal","aqua"]
		  });
		  
		  clearMarkers();
		  var marker;
		  
		  for(var x = 0;x < 34;x = x + 1){
			  var _r = raw_province_level[sentiment.index_province[x]];
			  var category;
			  var level;
			  if(_r != undefined){
				  if(_r[0] == 0){
					  category = "sad";
				  }
				  if(_r[0] == 1){
					  category = "angry";
				  }
				  if(_r[0] == 2){
					  category = "happy";
				  }
				  if(_r[1] == 0){
					  level = 2;
				  }
				  if(_r[1] == 1){
					  level = 2;
				  }
				  if(_r[1] == 2){
					  level = 3;
				  }
				  if(_r[1] == 3){
					  level = 3;
				  }
				  if(_r[1] == 4){
					  level = 4;
				  }
				  
				  var latlngs = sentiment.province_latlngs[x-1].split(" ");
				  //console.log(category);
				  //console.log(level);
				  marker = new google.maps.Marker({
					  icon : sentiment.markerIcons[category][level],
					  position : new google.maps.LatLng(latlngs[0],latlngs[1]),
				  });			  
				  markers.push(marker);
			  }
			  
		  }
		  
		  if(heatmap_type == 0){
			  for(var m = 0;m < markers.length;m = m + 1){
				  markers[m].setMap(map);
			  }
		  }
		  if(heatmap_type == 1){
			  heatmap1.setMap(map);
		  }
		  if(heatmap_type == 2){
			  heatmap2.setMap(map);
		  }
		  if(heatmap_type == 3){
			  heatmap2.setMap(map);
		  }
		  
	}
function formatFloat(src, pos){
    return Math.round(src*Math.pow(10, pos))/Math.pow(10, pos);
}
function check(){
	if(document.activeElement.id == "relativelimit"){
		if($("#absolutelimit").val() != $("#relativelimit").val() * sentiment.count / 100){
			 var result = parseInt($("#relativelimit").val() * sentiment.count / 100);
			 $("#absolutelimit").val(result);
		}
	}
	if(document.activeElement.id == "absolutelimit"){
		if($("#absolutelimit").val() != $("#relativelimit").val() * sentiment.count / 100){
			 var result = formatFloat($("#absolutelimit").val() * 100 / sentiment.count,2);
			 $("#relativelimit").val(result);
		}
	}
	
	setTimeout("check()",100);
}
function pageFailure(error){
	//window.location.href = "/weiming/mapweibo/error?page=sentimentview&status=" + error;
}
function initialize() {
	window.location.href = "#mapContainer";
	
	if(parseInt(sentiment.limit) <= 1000 || parseInt(sentiment.step_sum) > 100 || parseInt(sentiment.step_sum) <= 0){
		   pageFailure("sentiment_limit_illegal");
	}
	//console.log(sentiment.getPresentCollection);
	$.ajax({
		  url : '/mapweibo/mapcount?topic=' + sentiment.getPresentTopic + '&collection=' + sentiment.getPresentCollection,
		  cache: false,
		  dataType : 'json',   
		  type: "GET",   
		  success : function (data) {
			  sentiment.count = data.count;
			  $("#count").val("微博总数：" + sentiment.count);
			  if(parseInt(sentiment.count) <= 1000){
				  pageFailure("sentiment_count_little");
			  }
		  }
	});
	
	window.location.href = "#mapContainer";
	
    $("#mapContainer").block({
		message: '<h2><img src="/static/mapweibo/images/ajax_loader.gif" />数据加载中，请稍候...</h2>'
    });
	
	
	var request = '/mapweibo/sentimentview?topic=' + sentiment.getPresentTopic + '&limit=' + sentiment.limit + '&collection=' + sentiment.getPresentCollection;//+ '&starttime=' + sentiment.starttime + '&endtime=' + sentiment.endtime;
	$.ajax({
		  url : request,
		  cache: false,
		  dataType : 'json',   
		  type: "POST",   
		  success : function (data) {
			    raw_data = data;
				dataHandle();
				
				sentiment.step_sum = data.length;
				console.log(sentiment.step_sum); 
				$('#slider').slider({
					max: sentiment.step_sum + 1
				})
				
				initial_now_step();
				
				$('#slider').bind( 'slidechange', function(event, ui) {
					clearMarkers();
					clearHeatmap();
					var now_slider =  $('#slider').slider( "option", "value" );
					if(now_slider == 0){
						sentiment.now_step = -1;
					}
					else{
						sentiment.now_step = now_slider - 1;
					}
					if(sentiment.now_step == sentiment.step_sum){
						 date_div.innerText='当前时间';
						 static_data_display();
					}
					if(sentiment.now_step == -1){
						 date_div.innerText='当前时间';
					     static_data_display(); 
					}
				    if(sentiment.now_step >= 0 && sentiment.now_step < (sentiment.step_sum+2)){
						 change_date_display();
						 change_data_display();
						 change_map_display(); 
				    }
				 }); 
				
				$("#mapContainer").unblock();
				if (stoped==true) {
					stoped=false;					
					sentiment.inter_slider=setInterval(play_interval,sentiment.interval_time);
				}
		  },
		  error: function(jqXHR, textStatus, errorThrown) {
                console.log('error');
                console.log(errorThrown);
                console.log(jqXHR);
				pageFailure("sentimentview_broken_down");
          }
	  });
	 
	 function initial_now_step(){
		sentiment.now_step = -1;
	  }
					
     
	 
	 $('#play_pause1').click(function() {
		  if (stoped==true) {	  
			  stoped=false;
	  		  sentiment.inter_slider=setInterval(play_interval,sentiment.interval_time);
		  }
	 });
     $('#play_pause2').click(function() {
		  stoped=true;
	 });
	 $('#play_pause3').click(function() {
		  stoped=true;
		  date_div.innerText='';
		  $('#slider').slider( "option", "value",0);	
	 });
	
	function static_data_display(){
		 $(".section#left").empty();
		 $(".section#middle").empty();
		 $(".section#right").empty();
		 $(".section#left").append("<h2>原创微博省份数量累计</h2><ol id='most_fipost'></ol>");
		 $(".section#middle").append("<h2>转发微博省份数量累计</h2><ol id='most_repost'></ol>");
		 $(".section#right").append("<h2>微博总数累计</h2><ol id='most_post'></ol>");
		 var starttime = distinct_time[0];
		 var endtime = distinct_time[sentiment.step_sum-1];
	 }
	 
	function change_data_display(){
		$(".section#left").empty();
		 $(".section#middle").empty();
		 $(".section#right").empty();
		 $(".section#left").append("<h2>最高兴的省份</h2><ul id='most_happy'></ul>");
		 $(".section#middle").append("<h2>最生气的省份</h2><ul id='most_angry'></ul>");
		 $(".section#right").append("<h2>最悲伤的省份</h2><ul id='most_sad'></ul>");
		$("#most_happy").empty();
		$("#most_angry").empty();
		$("#most_sad").empty();
		
		var raw_most_province = raw_data[sentiment.now_step-1].most_province;
		var most_happy = raw_most_province[2];
		var most_angry = raw_most_province[1];
		var most_sad = raw_most_province[0];
		
		$("#most_happy").append("<li><span>" + most_happy[0] + "</span><br><span  class='weak'>高兴：" + most_happy[1][2] + "条微博</span><br><span class='weak'>生气：" + most_happy[1][1] + "条微博</span><br><span  class='weak'>悲伤：" + most_happy[1][0] + "条微博</span></li>");
		$("#most_angry").append("<li><span>" + most_angry[0] + "</span><br><span  class='weak'>高兴：" + most_angry[1][2] + "条微博</span><br><span class='weak'>生气：" + most_angry[1][1] + "条微博</span><br><span  class='weak'>悲伤：" + most_angry[1][0] + "条微博</span></li>");
		$("#most_sad").append("<li><span>" + most_sad[0] + "</span><br><span  class='weak'>高兴：" + most_sad[1][2] + "条微博</span><br><span class='weak'>生气：" + most_sad[1][1] + "条微博</span><br><span  class='weak'>悲伤：" + most_sad[1][0] + "条微博</span></li>");

	}
	
	function change_date_display(){
		if(distinct_time[sentiment.now_step]){
			//date_div.innerText="从 " + new Date(distinct_time[sentiment.now_step-1]*1000).format('yyyy-MM-dd hh:mm:ss') + " 至 " + new Date(distinct_time[sentiment.now_step]*1000).format('yyyy-MM-dd hh:mm:ss');
			date_div.innerText="第" + sentiment.now_step + "步" + new Date(distinct_time[sentiment.now_step]*1000).format('yyyy-MM-dd hh:mm:ss');
		}
		else{
			date_div.innerText="last part of time:" + new Date(distinct_time[sentiment.now_step-1]*1000).format('yyyy-MM-dd hh:mm:ss') + "-";
		}
	}

	
	function play_interval(){
		  if (stoped) {
			  if (sentiment.inter_slider!=null) {
			      clearInterval(sentiment.inter_slider);
			  }
		  } 
		  else {
			  if (sentiment.now_step < sentiment.step_sum  && sentiment.now_step >= -1) {	
			  	  $("#slider" ).slider("option", "value", ($("#slider" ).slider("option", "value") + 1));
			  }
			  if (sentiment.now_step == sentiment.step_sum) {	
			  	  $("#slider" ).slider("option", "value", 0);
			  }
			  console.log("sentiment.now_step:" + sentiment.now_step);
		  }
	}

}

$(function(){
    DOM.init();
	initialize();
});



