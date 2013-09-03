<!DOCTYPE HTML>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/_theme/reset.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/styles.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/syntax.css" type="text/css" />
    <title>pusto.org: {% block title %}{{ title or url }}{% endblock %}</title>
</head>
<body>
{% set github="https://github.com/naspeh/pusto/" %}
{% set github_data=github + "tree/master/data" %}
{% block header %}
<div class="header">
    <a class="logo" href="/">pusto.org</a>
    <ul class="nav">
        <li><a href="{{ github }}">исходники</a></li>
        <li><a href="/naspeh/">об авторе</a></li>
    </ul>
</div>
{% endblock %}
{% block body %}
    {% if html_title or title %}
    <div class="title">
        <h1>{{ html_title or title }}</h1>
        <ul class="meta">
            {% if published %}
            <li>Опубликовано: {{ published.strftime('%d.%m.%Y') }}</li>
            {% endif %}
            <li><a href="{{ github_data }}{{ index_file or url }}">смотреть на github</a></li>
        </li>
    </div>
    {% endif %}
    <div class="document">
        {{ html_body }}
    </div>
{% endblock %}
</body>
