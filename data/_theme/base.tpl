{% from '_theme/macros.tpl' import show_meta %}
<!DOCTYPE HTML>
{% set EN = p.params.lang == 'en' or p.parent.params.lang == 'en' %}
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
        <li class="link-logo"><a href="/" title="Russian part">pust<b>o.o</b>rg</a></li>
        <li><a href="/en/">en</a></li>
    </ul>
    <ul class="nav">
        <li><a href="/mailur/" title="Lightweight webmail inspired by Gmail">Mailur</a></li>
        <li><a href="/en/resume/">Résumé</a></li>
        <li><a href="/">Articles (Ru)</a></li>
        <li><a href="/trip/" title="Our trips">Trips (Ru)</a></li>
    </ul>
</div>
{% else %}
<div class="header">
    <ul class="nav logo">
        <li class="link-logo"><a href="/" title="Russian part">pust<b>o.o</b>rg</a></li>
        <li><a href="/en/" title="English part">en</a></li>
    </ul>
    <ul class="nav">
        <li><a href="/mailur/" title="Lightweight webmail inspired by Gmail">Mailur</a></li>
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
{% endblock %}

<!-- Hotjar Tracking Code for https://pusto.org -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:3130552,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
</body>
