(function ($) {
    'use strict';
    var defaults = {
        boxThumbsize: '72c',
        boxWidth: 3,
        boxHeight: 1,

        frontUseHash: true,
        frontThumbsize: '60c',
        frontCount: 8,

        // Picasa options
        picasaUser: 'naspeh',
        picasaAlbum: 'Naspeh',
        picasaAlbumid: '',
        picasaFilter: '',
        picasaIgnore: ''
    };
    var picasa = {
        fetch: function(opts, success) {
            var parts = ['user', opts.picasaUser];
            if (opts.picasaAlbumid) {
                parts = parts.concat(['albumid', opts.picasaAlbumid]);
            } else {
                parts = parts.concat(['album', opts.picasaAlbum]);
            }
            $.ajax({
                url: 'https://picasaweb.google.com/data/feed/api/' + parts.join('/'),
                data: {
                    kind: 'photo',
                    thumbsize: [opts.boxThumbsize, opts.frontThumbsize].join(',')
                },
                dataType: 'jsonp',
                success: function(data) {
                    success(picasa.parse(opts, data));
                },
                error: function(data, textStatus) {
                    console.error(
                        'Don\'t fetch data from picasaweb, status:', textStatus, data
                    );
                }
            });
        },
        parse: function(opts, data) {
            data = $(data);
            var albumId = data.find('gphoto\\:albumid:first').text();
            var items = [];
            data.find('entry').each(function() {
                var $this = $(this);
                var media = $this.find('media\\:group');
                var orig = media.find('media\\:content');
                var thumb = media.find('media\\:thumbnail').first();
                var thumb2 = media.find('media\\:thumbnail').last();
                var item = {
                    'id': $this.find('gphoto\\:id').text(),
                    'albumId': albumId,
                    'picasa': $this.find('link[rel="alternate"]').attr('href'),
                    'orig': {
                        url: orig.attr('url'),
                        width: orig.attr('width'),
                        height: orig.attr('height')
                    },
                    'boxThumb': {
                        url: thumb.attr('url'),
                        size: opts.boxThumbsizeInt
                    },
                    'frontThumb': {
                        url: thumb2.attr('url'),
                        size: opts.frontThumbsizeInt
                    },
                    'title': escapeHtml(media.find('media\\:title').text()),
                    'desc': escapeHtml(media.find('media\\:description').text()),
                    'tags': escapeHtml(media.find('media\\:keywords').text())
                };
                if (picasa.checkTags(opts, item.tags)) {
                    items.push(item);
                }
            });
            return {
                items: items,
                albumId: albumId,
                opts: opts
            };
        },
        checkTags: function(opts, tags) {
            tags = tags ? ',' + tags.split(', ').join(',') + ',' : '';
            var ignore = opts.picasaFilter && !opts.picasaFilter.test(tags);
            ignore = ignore || opts.picasaIgnore && opts.picasaIgnore.test(tags);
            return !ignore;
        },
        parseTags: function(tags) {
            tags = tags ? tags.split(',') : [];
            if ($.isArray(tags) && tags.length) {
                tags = tags.join(',|,');
                tags = new RegExp(',' + tags + ',');
            } else {
                tags = undefined;
            }
            return tags;
        }
    };
    var template = (
        // Box on page
        '<div class="napokaz-b">' +
            '{% $.each(items, function(num, item) { %}' +
            '{% if (!num) { %}' +
                '<div class="napokaz-b-page">' +
            '{% } %}' +
            '<div class="napokaz-b-thumb"' +
                'id="{{ item.id }}"' +
                'data-img="{{ item.boxThumb.url }}"' +
                'style="' +
                    'background-image: none;' +
                    'width: {{ item.boxThumb.size }}px;' +
                    'height: {{ item.boxThumb.size }}px"' +
            '>&nbsp;</div>' +
            '{% if ((items.length - num) === 1) { %}' +
                '</div>' +
            '{% } else if ((num + 1) % opts.boxWidth === 0) { %}' +
                '</div><div class="napokaz-b-page">' +
            '{% } %}' +
            '{% }); %}' +
        '</div>' +
        // Front
        '<div class="napokaz-f napokaz-f-ctrls">' +
            '<div class="napokaz-f-overlay">&nbsp;</div>' +
            '<div class="napokaz-f-orig">' +
                '<div class="napokaz-f-prev"><span>&lsaquo;</span></div>' +
                '<div class="napokaz-f-next"><span>&rsaquo;</span></div>' +
                '<div class="napokaz-f-close">&otimes;</div>' +
                '<div class="napokaz-f-img"></div>' +
                '<a class="napokaz-f-title" href="" target="_blank"></a>' +
            '</div>' +
            '<div class="napokaz-f-thumbs napokaz-f-ctrls">' +
                '<div class="napokaz-f-pprev"><span>&laquo;</span></div>' +
                '<div class="napokaz-f-pnext"><span>&raquo;</span></div>' +
                '<div class="napokaz-f-page">' +
                    '{% $.each(items, function(num, item) { %}' +
                    '<div class="napokaz-f-thumb"' +
                        'id="{{ item.id }}"' +
                        'data-title="{{ item.title }}"' +
                        'data-desc="{{ item.desc }}"' +
                        'data-href="{{ item.orig.url }}"' +
                        'data-size="[{{ item.orig.width }},{{ item.orig.height }}]"' +
                        'data-picasa="{{ item.picasa }}"' +
                        'data-img="{{ item.frontThumb.url }}"' +
                        'style="' +
                            'background-image: none;' +
                            'width: {{ item.frontThumb.size }}px;' +
                            'height: {{ item.frontThumb.size }}px"' +
                    '>&nbsp;</div>' +
                    '{% }); %}' +
                '</div>' +
            '</div>' +
        '</div>'
    );
    var main = function(opts, container) {
        var me = {
            process: function() {
                var box = container.find('.napokaz-b');
                var perPage = opts.boxWidth * opts.boxHeight;
                box.find('.napokaz-b-thumb').click(function() {
                    var front = container.find('.napokaz-f');
                    var current = front.find('#' + $(this).attr('id'));
                    me.initFront(front, current);
                    front.trigger('show');
                    front.trigger('select', current);
                    return false;
                });
                me.selector(box, 'napokaz-b-thumb', 'napokaz-b-show', perPage);
                box.trigger('page:select', box.find('.napokaz-b-thumb:first'));
                if (!$('.napokaz-f:visible').length) {
                    box.find(window.location.hash).click();
                }
            },
            initFront: function(front, current) {
                if (front.data('initOnce')) {
                    return;
                }
                front.data('initOnce', true);

                var count = front.find('.napokaz-f-thumb').length;
                if (count === 1) {
                    front.removeClass('napokaz-f-ctrls');
                } else if (count <= opts.frontCount) {
                    front.find('.napokaz-f-thumbs').removeClass('napokaz-f-ctrls');
                }

                me.selector(front, 'napokaz-f-thumb', 'napokaz-f-current');
                me.selector(front, 'napokaz-f-thumb', 'napokaz-f-show', opts.frontCount);
                front.on({
                    'show': function() {
                        $(this).show();
                    },
                    'hide': function() {
                        $(this).hide();
                        if (opts.frontUseHash) {
                            window.location.hash = '';
                        }
                    },
                    'select': function(e, thumb) {
                        thumb = $(thumb);
                        if (!thumb.hasClass('napokaz-f-show')) {
                            front.trigger('page:select', thumb);
                        }
                        me.getImg(front, thumb);
                        var preloads = [
                            thumb.next('.napokaz-f-thumb'),
                            thumb.prev('.napokaz-f-thumb')
                        ];
                        $.each(preloads, function() {
                            if (this.length) {
                                me.getImg(front, this, true);
                            }
                        });
                        if (opts.frontUseHash) {
                            window.location.hash = thumb.attr('id');
                        }
                    }
                });
                front.find('.napokaz-f-thumb').click(function() {
                    front.trigger('select', this);
                    return false;
                });
                var events = [
                    ['.napokaz-f-close', 'hide'],
                    ['.napokaz-f-prev', 'prev'],
                    ['.napokaz-f-next', 'next'],
                    ['.napokaz-f-pprev', 'page:prev'],
                    ['.napokaz-f-pnext', 'page:next']
                ];
                $.each(events, function(i, item) {
                    front.find(item[0]).on('click', function() {
                        front.trigger(item[1]);
                        return false;
                    });
                });

                swipe(front.find('.napokaz-f-next, .napokaz-f-prev'), function(delta) {
                    front.trigger((delta && delta < 0) ? 'prev': 'next');
                });
                swipe(front.find('.napokaz-f-thumb'), function(delta) {
                    front.trigger((delta && delta < 0) ? 'page:prev': 'page:next');
                });

                // Set navigation key bindings
                $(document).on('keydown.napokaz-f', function (e) {
                    if (front.is(':hidden')) {
                        return;
                    }
                    var events = {
                        8: 'hide', // Backspace
                        27: 'hide', // Esc
                        46: 'hide', // Delete
                        37: 'prev', // <=
                        39: 'next', // =>
                        33: 'page:prev', // PageUp
                        34: 'page:next' // PageDown
                    };
                    if (events.hasOwnProperty(e.keyCode)) {
                        e.preventDefault();
                        front.trigger(events[e.keyCode]);
                    }
                });
            },
            selector: function(box, elementCls, currentCls, perPage) {
                perPage = !perPage ? 0 : perPage;
                var prefix = perPage > 1 ? 'page:' : '';
                var elementSel = '.' + elementCls;
                var currentSel = '.' + currentCls;
                var selector = function(e) {
                    var cur, el, isNext;
                    isNext = e.data.isNext;
                    cur = box.find(currentSel + (isNext ? ':last': ':first'));
                    el = cur[isNext ? 'next': 'prev'](elementSel);
                    if (!el.length) {
                        el = box.find(elementSel + (isNext ? ':first': ':last'));
                    }
                    box.trigger(prefix + 'select', el);
                };
                box.on(prefix + 'prev', {isNext: false}, selector);
                box.on(prefix + 'next', {isNext: true}, selector);
                box.on(prefix + 'select', function(e, element) {
                    element = $(element);
                    box.find(currentSel).removeClass(currentCls);
                    if (perPage <= 1) {
                        element.addClass(currentCls);
                        return;
                    }
                    var items = box.find(elementSel);
                    var current = items.index(element);
                    current = Math.floor(current / perPage) * perPage;
                    items = items.slice(current, current + perPage).addClass(currentCls);
                    items.each(function() {
                        var $this = $(this);
                        var url = $this.data('img');
                        if (url) {
                            $this.css({'background-image': 'url(' + url  + ')'});
                        }
                    });
                });
            },
            getImg: function(front, thumb, preloadOnly) {
                var box = front.find('.napokaz-f-orig');
                box.css({
                    'bottom': front.find('.napokaz-f-thumbs').outerHeight(true)
                });
                var img = thumb.data();
                var url = (
                    img.href + '?imgmax=' +
                    me.getImgMax(img.size, [box.width(), box.height()])
                );
                if (preloadOnly) {
                    $('<img/>').attr('src', url);
                    return;
                }
                box.css({'background-image': 'url(' + url  + ')'});
                front.find('.napokaz-f-title')
                    .html(img.desc || img.title)
                    .attr('href', img.picasa);
            },
            getImgMax: function(img, win) {
                img = {w:img[0], h:img[1]};
                win = {w:win[0], h:win[1]};

                var ratio, result;
                ratio = img.w / img.h;
                ratio = ratio > 1 && ratio || 1;
                result = Math.min(win.h * ratio, win.w);
                result = Math.round(result);
                return result;
            }
        };
        return me;
    };

    // Public {{{
    $.fn.napokaz = function(options) {
        options = $.extend({}, $.fn.napokaz.defaults, options);
        return this.each(function() {
            var container = $(this);
            var opts = preOptions($.extend({}, options, container.data()));
            picasa.fetch(opts, function(data) {
                console.log(data);
                container.html(tmpl(template, data));
                main(opts, container).process();
            });

        });
    };
    $.fn.napokaz.defaults = defaults;
    $.fn.napokaz.defaults.set = function(options) {
        $.fn.napokaz.defaults = $.extend({}, $.fn.napokaz.defaults, options);
    };
    // }}}

    // Functions
    function preOptions(o) {
        o.boxThumbsizeInt = parseInt(o.boxThumbsize, 10);
        o.frontThumbsizeInt = parseInt(o.frontThumbsize, 10);
        o.picasaFilter = picasa.parseTags(o.picasaFilter);
        o.picasaIgnore = picasa.parseTags(o.picasaIgnore);
        return o;
    }

    function swipe(elements, callback) {
        $.each(elements, function(i, element) {
            var x, delta,
            check = function(callback) {
                return function(event) {
                    if (event.touches.length == 1 || event.scale && event.scale !== 1) {
                        callback(event);
                    }
                    event.preventDefault();
                };
            },
            handler = {
                handleEvent: function(event) {
                    switch (event.type) {
                        case 'touchstart': this.start(event); break;
                        case 'touchmove': this.move(event); break;
                        case 'touchend': this.end(event); break;
                    }
                },
                start: check(function(event) {
                    x = event.touches[0].pageX;
                    element.addEventListener('touchmove', handler, false);
                    element.addEventListener('touchend', handler, false);
                }),
                move: check(function(event) {
                    delta = x - event.touches[0].pageX;
                }),
                end: function(event) {
                    if (x && delta === undefined) {
                        $(element).click();
                    } else if (Math.abs(delta) > 50) {
                        callback(delta);
                    } else {
                        event.preventDefault();
                    }
                    x = undefined;
                    delta = undefined;
                    element.removeEventListener('touchmove', handler, false);
                    element.removeEventListener('touchend', handler, false);
                }
            };
            if (!!window.addEventListener) {
                element.addEventListener('touchstart', handler, false);
            }
        });
    }

    // Taken from mustache.js
    var entityMap = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': '&quot;',
        "'": '&#39;',
        "/": '&#x2F;'
    };
    function escapeHtml(string) {
        return String(string).replace(/[&<>"'\/]/g, function (s) {
            return entityMap[s];
        });
    }

    // Taken from underscore.js with reformating and another delimiters.
    // JavaScript micro-templating, similar to John Resig's implementation.
    // Underscore templating handles arbitrary delimiters, preserves whitespace,
    // and correctly escapes quotes within interpolated code.
    function tmpl(str, data) {
        var c = {
            evaluate    : /\{%([\s\S]+?)%\}/g,
            interpolate : /\{\{([\s\S]+?)\}\}/g
        };
        var fn = new Function('obj',
            "var __p=[];" +
            "var print = function() {" +
                "__p.push.apply(__p, arguments);" +
            "};" +
            "with(obj || {}) {" +
                "__p.push('" +
                    str
                    .replace(/\\/g, '\\\\')
                    .replace(/'/g, "\\'")
                    .replace(c.interpolate, function(match, code) {
                        return "'," + code.replace(/\\'/g, "'") + ",'";
                    })
                    .replace(c.evaluate || null, function(match, code) {
                        code = code.replace(/\\'/g, "'").replace(/[\r\n\t]/g, ' ');
                        return "');" + code + "__p.push('";
                    })
                    .replace(/\r/g, '\\r')
                    .replace(/\n/g, '\\n')
                    .replace(/\t/g, '\\t') +
                "');" +
            "}" +
            "return __p.join('');"
        );
        return data ? fn(data) : fn;
    }
}(jQuery));
if (!window.console) {
    window.console = {
        log: function() {},
        error: function() {}
    };
}
