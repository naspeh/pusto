{% from '_theme/macros.tpl' import show_meta %}
<!DOCTYPE HTML>
<head>
{% block head %}
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/_theme/reset.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/styles.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/syntax.css" type="text/css" />
    <link rel="stylesheet" href="http://cdn.jsdelivr.net/qtip2/2.2.0/jquery.qtip.min.css" type="text/css" />
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
</div>
{% endblock %}
<script src="http://code.jquery.com/jquery.js"></script>
<script src="http://cdn.jsdelivr.net/qtip2/2.2.0/jquery.qtip.min.js"></script>
<script>
    var cache = null;
    $.get('/terms.html').then(function(data) {
        cache = $(data);
    }).then(function() {
        $('a[href^="/terms.html"]').each(function() {
            var $this = $(this);
            $this.click(function(event) {
                event.preventDefault();
            });

            var term = $this.attr('href').replace('/terms.html#', '');
            term = cache.find('#' + term);
            $this.qtip({
                content: {
                    title: term.find('dt').html(),
                    text: term.find('dd').html(),
                    button: true
                },
                show: 'click',
                hide: 'unfocus'
            });
        });
    });
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
