{% from '_theme/macros.tpl' import show_meta %}
<!DOCTYPE HTML>
<head>
{% block head %}
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/all.css?{{ p.pages['/all.css'].mtime }}" type="text/css" />
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
