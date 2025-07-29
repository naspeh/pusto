{% from '_theme/macros.tpl' import show_meta %}
<!DOCTYPE HTML>
{% set EN = p.params.lang != 'ru' and p.parent.params.lang != 'ru' %}
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
        <li class="link-logo"><a href="/">pust<b>o.o</b>rg</a></li>
    </ul>
    <ul class="nav">
        <li><a href="/mailur/" title="Lightweight webmail inspired by Gmail">Mailur</a></li>
        <li><a href="/resume/">Résumé</a></li>
        <li><a href="https://www.behance.net/naspeh">Photos</a></li>
    </ul>
</div>
{% else %}
<div class="header">
    <ul class="nav logo">
        <li class="link-logo"><a href="/">pust<b>o.o</b>rg</a></li>
    </ul>
    <ul class="nav">
        <li><a href="/mailur/" title="Lightweight webmail inspired by Gmail">Mailur</a></li>
        <li><a href="/post/">Статьи</a></li>
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
</body>
