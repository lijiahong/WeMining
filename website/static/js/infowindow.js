var infoWindow = (function () {
    var currMarker = {},
        leftOffset = -180,
        html = '<div id="info-window"><div class="inner clearfix"></div></div>',
        $elm,
        $elmInner,
        visible = false,
        loading = false;
        return {
            newPosition : function (latLng) {
                var pixelPoint = projection.fromLatLngToContainerPixel(latLng);
                var winWidth = $(document).width();
                var elmWidth = $elm.width();
                var elmHeight = $elm.height();
                var leftBorder = pixelPoint.x - leftOffset;
                var rightBorder = pixelPoint.x - leftOffset + elmWidth;
                var topBorder = pixelPoint.y -  elmHeight;
                var panByX = 0;
                var panByY = 0;
                if (rightBorder > winWidth) 
                    panByX = rightBorder - winWidth + 20;
                if (rightBorder < winWidth && rightBorder > winWidth - 20) 
                    panByX = 20 - (winWidth - rightBorder);
                if (leftBorder < 0) panByX = leftBorder - 20;
                if (leftBorder > 0 && leftBorder < 20) 
                    panByX = -1 * (20 - leftBorder);
                if (topBorder < 0) 
                    panByY = topBorder - 40;
                if (topBorder > 0 && topBorder < 40) 
                    panByY = -1 * (40 - topBorder);
                map.panBy(panByX, panByY);
                pixelPoint = projection.fromLatLngToContainerPixel(latLng);
                $elm.css({
                    left: pixelPoint.x - leftOffset + 'px',
                    top: pixelPoint.y - ($elm.height()-35) + 'px'
                });
            },
            close : function () {
                if ( !loading && visible ) {
                    $elm.css({ left: '-9999px' });
                    $elm.removeClass('video').find('.thumb').removeClass('hidden').siblings('.video').html('');
                    visible = false;
                }
            },
            init: function () {
                $elm = $('body').append(html).find('#info-window');
                $elmInner = $elm.find('.inner');
            },
            open: function (marker) {
                if ( marker.id === currMarker.id && loading ) {
                    $elmInner.html('').append(marker.content);
                    
					loading = false;
					$elm.removeClass('loading');
					infoWindow.newPosition( marker.getPosition() );
                    
                } else if ( marker.id !== currMarker.id || !visible ) {
                    infoWindow.close();
                    $elmInner.html('').append(marker.content);
                    currMarker = marker;
                    infoWindow.newPosition( marker.getPosition() );
                    visible = true;
                }
            },
            preload: function (marker) {
                if ( !loading ) {
                    currMarker = marker;
                    $elm.addClass('loading');
                    loading = true;
                    visible = true;
                    infoWindow.newPosition( currMarker.getPosition() );
                    
                    marker.content = '<h2> original ' + marker.fipost + '</h2>' +  '<h2> forward ' + marker.repost + '</h2>';            
                    infoWindow.open(marker);
                }
                
            },
            
        };
})();

MarkerClusterer.prototype.getClusters_ = function(){
	return this.clusters_;
}