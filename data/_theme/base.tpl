{% from '_theme/macros.tpl' import show_meta %}
<!DOCTYPE HTML>
<head>
{% block head %}
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/_theme/reset.css" type="text/css" />
    <link rel="stylesheet" href="http://cdn.jsdelivr.net/qtip2/2.2.0/jquery.qtip.min.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/styles.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/syntax.css" type="text/css" />
    <script src="http://code.jquery.com/jquery.js"></script>

    <link rel="stylesheet" href="/s/napokaz/src/napokaz.css" />
    <style>
        .napokaz {
            display: inline-block;
            *display: inline;
            *zoom: 1;
            margin: 0 5px;
            margin-bottom: 1em;
            vertical-align: top;
        }
    </style>
    <script src="/s/napokaz/src/napokaz.js"></script>
    {% if not napokaz_skip %}
    <script>
    $(document).ready(function() {
        $.fn.napokaz.defaults.set({
            boxThumbsize: '100c',
            frontCount: 10,
            frontThumbsize: '60c',
            frontUseHash: false,
            picasaIgnore: 'hide'
        });
        $('.napokaz').napokaz();
    });
    </script>
    {% endif %}
    <title>pusto.org: {% block title %}{{ p.title|striptags or p.url }}{% endblock %}</title>
{% endblock %}
</head>

<body>
{% block header %}
<div class="header">
    <a class="logo" href="/">pusto.org</a>
    <ul class="nav">
        <li><a href="/trip/">Наши поездки</a></li>
        <li><a href="/naspeh/">Об авторе</a></li>
    </ul>
</div>
{% endblock %}
{% block body %}
<div itemscope="itemscope" itemtype="http://schema.org/Article">
    {% if p.title %}
    <div class="title">
        <h1 itemprop="name">{{ p.title }}</h1>
        <link itemprop="url" href="{{ url }}" />
        {{ show_meta(p, back_url=True)}}
    </div>
    {% endif %}
    <div class="document">
        {% block document %}
        {{ p.body }}
        {% endblock%}
    </div>
    {% if p.terms %}
    <hr />
    <div class="terms">
        <h3 class="terms-title"><a href="#">Используемые термины</a></h3>
        <div class="terms-body">
            {{ p.terms }}
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
<script src="http://cdn.jsdelivr.net/qtip2/2.2.0/jquery.qtip.min.js"></script>
<script>
    $('.terms').click(function() {
        $(this)
            .toggleClass('terms-hide')
            .find('.term-active').removeClass('term-active');
    });
    $('a[href^="#term-"]').each(function() {
        var $this = $(this);
        var term = $($this.attr('href'));

        $this.addClass('term')
        $this.click(function(event) {
            event.preventDefault();
            var cls = 'term-active';
            $('.terms .' + cls).removeClass(cls)
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
                    $this.find('.napokaz').napokaz();
                    $this.find('.napokaz-b-thumb').click(function () {
                        var tooltip = api.elements.tooltip;
                        tooltip.hide();
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
    if (location.hash.indexOf('#term-') == 0) {
        var term = location.hash
        $(term).addClass('term-active');
    } else {
        $('.terms').addClass('terms-hide')
    }
</script>

<script>
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-6254112-1']);
    _gaq.push(['_trackPageview']);

    (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();
</script>
</body>
