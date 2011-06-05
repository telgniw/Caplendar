(function($) {
    var $dialog = $('<div></div>');
    $.fn.closeButton = function() {
        return this.each(function() {
            $(this).addClass('ui-icon ui-icon-close ui-corner-all').mouseenter(function() {
                $(this).addClass('ui-icon-closethick');
            }).mouseleave(function() {
                $(this).removeClass('ui-icon-closethick');
            });
        });
    };
    $.fn.deletable = function(options) {
        /** title:      dialog title    <optional>
            text:       dialog content  <optional>
            textDelete: delete button   <optional>
            textCancel: cancel button   <optional>
            onDelete:   function        <optional>
            onCancel:   function        <optional>
        **/
        var args = {
            title: 'Confirm',
            text: 'Delete?',
            textCancel: 'No',
            textDelete: 'Yes',
            onCancel: function() {},
            onDelete: function() {}
        };
        return this.each(function() {
            if(options)
                $.extend(args, options);
            var target = this;
            var close = $('<span></span>').css('float', 'right').click(function() {
                var buttons = [{
                        text: args.textDelete,
                        click: function() {
                            $(this).dialog('close');
                            args.onDelete.call(target);
                        }
                    }, {
                        text: args.textCancel,
                        click: function() {
                            $(this).dialog('close');
                            args.onCancel.call(target);
                        }
                    }
                ];
                $dialog.html(args.text).dialog({
                    autoOpen: true,
                    buttons: buttons,
                    dialogClass: 'alert',
                    draggable: false,
                    modal: true,
                    resizable: false,
                    title: args.title
                });
            }).closeButton();
            $(this).hover(function() {
                $(this).prepend(close);
                $(this).css({
                    cursor: 'pointer'
                }).addClass('ui-state-hover');
            }, function() {
                $(close).detach();
                $(this).css({
                    cursor: 'auto'
                }).removeClass('ui-state-hover');
            });
        });
    };
    $.fn.draggalist = function(options) {
        /** css:        {}              <optional>
            type:       tag name        <optional>
        **/
        var args = {
            css: {},
            type: 'div'
        };
        return this.each(function() {
            if(options)
                $.extend(args, options);
            args.css.overflow = 'hidden';
            $(this).css(args.css).addClass('ui-widget-content ui-corner-all');
            $(args.type+':only-child', this).each(function() {
                $(this).css('margin', '10px').draggable({
                    axis: 'y',
                    stop: function(evt, ui) {
                        var pos = $(this).position();
                        var h = $(this).height(), parent_h = $(this).parent().height();
                        if(pos.top > 0) {
                            $(this).animate({
                                top: '0px'
                            });
                        } else if(pos.top + h < parent_h) {
                            $(this).animate({
                                top: (parent_h-h-20) + 'px'
                            });
                        }
                    }
                });
                $(args.type, this).each(function() {
                    $(this).css({
                        display: 'block',
                        padding: '5px'
                    }).addClass('ui-priority-secondary ui-state-default ui-corner-all');
                });
            });
        });
    };
})(jQuery);