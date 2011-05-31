(function($) {
    var latlng = function(pos) {
        return new google.maps.LatLng(pos[0], pos[1]);
    }
    var image = function(color) {
        return 'http://www.google.com/mapfiles/ms/micons/' + color + '.png';
    }
    var default_position = latlng([23.5, 121]);
    $.fn.gmap = function(options) {
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
                if($.type(args.info.place) == 'array')
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
                $(marker).data('info', args.info);
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
    $.fn.get_info = function(key) {
        var markers = $(this[0]).data('markers');
        return $(markers[key]).data('info');
    };
    $.fn.set_info = function(key, type) {
        var target = this[0];
        var markers = $(target).data('markers');
        var info = $(markers[key]).data('info');
        if(info) {
            switch(type) {
                case 'center':
                    var map = $(target).data('map');
                    map.setCenter(latlng(info.place));
                    break;
            }
        }
        return this;
    };
})(jQuery);