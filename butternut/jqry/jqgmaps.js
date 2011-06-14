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
                        map.setZoom(18);
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
            google.maps.event.addListener(map, 'dblclick', function(evt) {
                var loc = evt.latLng;
                var func = $(target).data('prompt');
                func([loc.lat(), loc.lng()]);
            });
        });
    };
    $.fn.mark = function(options) {
        /** key:        key for delete  <required>
            uid:        user id         <required>
            info:       event info      <required>
            img:        icon image      <optional>
            background: icon background <optional>
            onClick:    marker clicked  <optional>
            onDrop:     marker dropped  <optional>
        **/
        var args = {
            color: 'red',
            onClick: function() {},
            onDrop: function() {}
        };
        return this.each(function() {
            var map = $(this).data('map');
            if(!map)
                return;
            var markers = $(this).data('markers');
            if(options)
                $.extend(args, options);
            var marker = false;
            if(markers[args.key]) {
                marker = markers[args.key].marker;
                if(marker)
                    marker.setMap(null);
            }
            var pos = args.info.place;
            if(!args.info.place)
              pos = map.getCenter();
            if($.type(pos) == 'array')
                pos = latlng(args.info.place);
            var time = args.info.time.replace(/^[0-9]{4}-[0-9]{2}-[0-9]{2}/, '');
            if(args.background) {
                marker = new MarkerWithLabel({
                    map: map,
                    position: pos,
                    title: args.info.name + ' ' + time,
                    icon: new google.maps.MarkerImage(args.img, new google.maps.Size(50,50), new google.maps.Point(0,0), new google.maps.Point(10,30), new google.maps.Size(20,20)),
                    shadow: new google.maps.MarkerImage(args.background, new google.maps.Size(32,36), new google.maps.Point(0,0), new google.maps.Point(16,36)),
                    shape: { coord: [-2,-2,-2,38,34,38,34,-2], type: 'poly' },
                    zIndex: 0
                });
            }
            else {
                marker = new MarkerWithLabel({
                    map: map,
                    position: pos,
                    draggable: true,
                    title: args.info.name + ' ' + time,
                    icon: new google.maps.MarkerImage(args.img, new google.maps.Size(50,32), new google.maps.Point(0,0), new google.maps.Point(25,32)),
                    shape: { coord: [-2,-2,-2,34,52,34,52,-2], type: 'poly' },
                    labelContent: time,
                    labelAnchor: new google.maps.Point(20,22),
                    labelStyle: { color: 'lightyellow', fontWeight: 'bold' }
                });
            }
            var target = this;
            if(args.onClick) {
              google.maps.event.addListener(marker, 'click', function() {
                args.onClick.call(target, args.key);
              });
            }
            if(args.onDrop) {
              google.maps.event.addListener(marker, 'dragend', function(evt) {
                var pos = evt.latLng;
                args.onDrop.call(target, { 'event-key': args.key, 'event-place': pos.lat() + ',' + pos.lng() });
              });
            }
            markers[args.key] = { marker: marker, uid: args.uid };
        });
    };
    $.fn.unmark = function(options) {
        /** key:        key for delete  <required>
        **/
        var args = {
        };
        return this.each(function() {
            var map = $(this).data('map');
            if(!map)
                return;
            var markers = $(this).data('markers');
            switch(options) {
                case 'all':
                    for(i in markers)
                      markers[i].marker.setMap(null);
                    return;
                case 'uid':
                    for(i in markers) {
                      if(!markers[i].uid)
                        markers[i].marker.setMap(null);
                    }
                    return;
            }
            if(options)
                $.extend(args, options);
            var marker = markers[args.key].marker;
            if(marker)
                marker.setMap(null);
        });
    };
})(jQuery);