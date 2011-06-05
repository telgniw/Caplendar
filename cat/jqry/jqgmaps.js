(function($) {
    var latlng = function(pos) {
        return new google.maps.LatLng(pos[0], pos[1]);
    }
    var image = function(color) {
        return 'http://www.google.com/mapfiles/ms/micons/' + color + '.png';
    }
    var default_position = latlng([23.5, 121]);
    $.fn.gmap = function(options, others) {
        /** position:   [lat, lng]      <required>
            template:   template        <required>
            css:        css map         <optional>
            zoom:       number          <optional>
        **/
        var args = {
            css: {},
            zoom: 7
        };
        return this.each(function() {
            switch(options) {
                case 'center':
                    if(others.place) {
                        var map = $(this).data('map');
                        map.setCenter(latlng(others.place));
                    }
                    return;
            }
            if(options)
                $.extend(args, options);
            var target = this;
            $(this).css(args.css);
            var pos = args.position;
            if($.type(args.position) == 'array')
                pos = latlng(args.position);
            var map = new google.maps.Map($(this)[0], {
                disableDoubleClickZoom: true,
                zoom: args.zoom,
                center: pos,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            });
            $(this).data({
                map: map,
                markers: {}
            });
            google.maps.event.addListener(map, 'click', function(evt) {
                var loc = evt.latLng;
                var func = $(target).data('prompt');
                func([loc.lat(), loc.lng()]);
            });
        });
    };
    $.fn.mark = function(options) {
        /** key:        key for delete  <required>
            info:       event info      <required>
            color:      icon color      <optional>
            onClick:    marker clicked  <optional>
        **/
        var args = {
            color: 'red',
            onClick: function() {}
        };
        return this.each(function() {
            if(options)
                $.extend(args, options);
            var map = $(this).data('map');
            if(map) {
                var markers = $(this).data('markers');
                var marker = markers[args.key];
                if(marker)
                    marker.setMap(null);
                var pos = args.info.place;
                if($.type(pos) == 'array')
                    pos = latlng(args.info.place);
                marker = new google.maps.Marker({
                    map: map,
                    position: pos,
                    title: args.info.name,
                    icon: image(args.color)
                });
                var target = this;
                google.maps.event.addListener(marker, 'click', function() {
                  args.onClick.call(target, args.key);
                });
                markers[args.key] = marker;
            }
        });
    };
    $.fn.unmark = function(options) {
        /** key:        key for delete  <required>
        **/
        var args = {
        };
        return this.each(function() {
            if(options)
                $.extend(args, options);
            var map = $(this).data('map');
            if(map) {
                var markers = $(this).data('markers');
                var marker = markers[args.key];
                if(marker)
                    marker.setMap(null);
            }
        });
    };
})(jQuery);