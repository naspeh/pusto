// {{ '\n' + load_file('_theme/libs/jquery.min.js') }}

// Init napokaz.js
// {{ '\n' + load_file('s/napokaz/src/napokaz.js') }}
(function($) {
    $.fn.napokaz.defaults.set({
        boxThumbsize: '100c',
        frontCount: 10,
        frontThumbsize: '60c',
        frontUseHash: false,
        picasaIgnore: 'hide'
    });
}(jQuery));


// Terms stuff
// {{ '\n' + load_file('_theme/libs/jquery.qtip.min.js') }}
(function($) {
    $('.napokaz-term').napokaz();
    $('.terms').click(function() {
        $(this)
            .toggleClass('terms-hide')
            .find('.term-active').removeClass('term-active');
    });
    $('a[href^="#term-"]').each(function() {
        var $this = $(this);
        var term = $($this.attr('href'));

        $this.addClass('term');
        $this.click(function(event) {
            event.preventDefault();
            var cls = 'term-active';
            $('.terms .' + cls).removeClass(cls);
            term.addClass(cls);
        });
        $this.qtip({
            overwrite: true,
            content: {
                title: term.find('dt').html(),
                text: term.find('dd').html(),
                button: true
            },
            show: {
                event: 'mouseenter click',
                effect: function(api) {
                    $this = $(this);
                    $this.show();
                    $this.find('.napokaz-term').napokaz();
                    $this.find('.napokaz-b-thumb').click(function () {
                        api.elements.tooltip.hide();
                        $('.terms').removeClass('terms-hide');
                        term.find('#' + $(this).attr('id')).click();
                    });
                }
            },
            hide: {
                fixed: true,
                delay: 300
            }
        });
    });
    if (location.hash.indexOf('#term-') === 0) {
        var term = location.hash;
        $(term).addClass('term-active');
    } else {
        $('.terms').addClass('terms-hide');
    }
}(jQuery));

// GA
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-6254112-1']);
_gaq.push(['_trackPageview']);

(function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
