{% from '_theme/macros.tpl' import show_meta %}

<!DOCTYPE HTML>
<head>
{% block head %}
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/_theme/reset.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/styles.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/syntax.css" type="text/css" />
    <title>pusto.org: {% block title %}{{ title|striptags or url }}{% endblock %}</title>
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
    {% if title %}
    <div class="title">
        <h1 itemprop="name">{{ title }}</h1>
        <link itemprop="url" href="{{ url }}" />
        {{ show_meta(page, back_url=True)}}
    </div>
    {% endif %}
    <div class="document">
        {% block document %}
        {{ body }}
        {% endblock%}
    </div>
</div>
{% endblock %}
<script type="text/javascript">
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
