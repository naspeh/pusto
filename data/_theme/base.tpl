{% from '_theme/macros.tpl' import show_meta %}
<!DOCTYPE HTML>
{% set EN = p.params.lang == 'en' %}
<head>
{% block head %}
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/all.css?{{ p.pages['/all.css'].mtime }}" type="text/css" />
    <title>pusto.org: {% block title %}{{ p.title|striptags or p.url }}{% endblock %}</title>
{% endblock %}
</head>

<body>
{% block header %}
{% if EN %}
<div class="header">
    <ul class="nav logo">
        <li><a href="/" title="Russian part">pusto.org</a></li>
        <li><a href="/en/">en</a></li>
    </ul>
    <ul class="nav">
        <li><a href="/en/resume/">Résumé</a></li>
        <li><a href="/">Articles (Ru)</a></li>
        <li><a href="/trip/">Trips (Ru)</a></li>
    </ul>
</div>
{% else %}
<div class="header">
    <ul class="nav logo">
        <li><a href="/">pusto.org</a></li>
        <li><a href="/en/" title="English part">en</a></li>
    </ul>
    <ul class="nav">
        <li><a href="/trip/">Наши поездки</a></li>
        <li><a href="/naspeh/">Об авторе</a></li>
    </ul>
</div>
{% endif %}
{% endblock %}


{% block body %}
<div itemscope="itemscope" itemtype="http://schema.org/Article">
    {% if p.title %}
    <div class="title">
        <h1 itemprop="name">{{ p.title }}</h1>
        <link itemprop="url" href="{{ url }}" />
        {{ show_meta(p, back_url=True, EN=EN)}}
    </div>
    {% endif %}
    <div class="document">
        {% block document %}
        {{ p.body }}
        {% endblock%}
    </div>
    {% if p.terms %}
    <hr />
    <div class="terms" id="terms">
        <h3 class="terms-title"><a href="#terms">{{ p.terms.title }}</a></h3>
        <div class="terms-body group">
            {{ p.terms.body }}
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block js %}
<script src="/all.js?{{ p.pages['/all.js'].mtime }}"></script>
<!-- Fathom - simple website analytics - https://github.com/usefathom/fathom -->
<script>
(function(f, a, t, h, o, m){
    a[h]=a[h]||function(){
        (a[h].q=a[h].q||[]).push(arguments)
    };
    o=f.createElement('script'),
    m=f.getElementsByTagName('script')[0];
    o.async=1; o.src=t; o.id='fathom-script';
    m.parentNode.insertBefore(o,m)
})(document, window, '//yadro.org/tracker.js', 'fathom');
fathom('set', 'siteId', 'CWDIE');
fathom('trackPageview');
</script>
<!-- / Fathom -->
{% endblock %}
</body>
