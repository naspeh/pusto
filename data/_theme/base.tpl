<!DOCTYPE HTML>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/_theme/reset.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/styles.css" type="text/css" />
    <title>pusto.org: {% block title %}{{ title or url }}{% endblock %}</title>
</head>
<body>
{% set github="https://github.com/naspeh/pusto/tree/master/data" %}
{% block body %}
    {% if html_title %}
    <h1 class="title">
        {{ html_title }}
        <ul class="title-meta">
            {% if created %}
            <li>Опубликовано: {{ created }}</li>
            {% endif %}
            <li><a href="{{ github }}{{ index_file }}">смотреть на github</a></li>
        </li>
    </h1>
    {% endif %}
    {{ html_body }}
{% endblock %}
</body>
