<!DOCTYPE HTML>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/_theme/reset.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/styles.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/syntax.css" type="text/css" />
    <title>pusto.org: {% block title %}{{ title|striptags or url }}{% endblock %}</title>
    {% block head_extra %}{% endblock %}
</head>
<body>
{% set github="https://github.com/naspeh/pusto/" %}
{% set github_data=github + "tree/master/data" %}
{% block header %}
<div class="header">
    <a class="logo" href="/">pusto.org</a>
    <ul class="nav">
        <li><a href="/naspeh/">об авторе</a></li>
    </ul>
</div>
{% endblock %}
{% block body %}
<div itemscope="itemscope" itemtype="http://schema.org/Article">
    {% if title %}
    <div class="title" itemprop="name">
        <h1>{{ title }}</h1>
        <link itemprop="url" href="{{ url }}" />
        <ul class="meta">
            {% if published %}
            <li itemprop="datePublished" datetime="{{ published.strftime('%Y-%m-%d')}}" >
                Опубликовано: {{ published.strftime('%d.%m.%Y') }}
            </li>
            {% endif %}
            {% if markup in ['md', 'rst'] %}
            <li><a href="{{ index_file }}">{{ markup }} текст</a></li>
            {% endif %}
            <li><a href="{{ github_data }}{{ index_file or url }}">смотреть на github</a></li>
        </li>
    </div>
    {% endif %}
    <div class="document">
        {{ body }}
    </div>
</div>
{% endblock %}
</body>
