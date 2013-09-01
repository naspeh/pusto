{% extends '_theme/base.tpl' %}
{% block body %}
<ul class="posts">
{% for url, child in children.items() %}
    <li class="post{% if loop.index == 1 %}post-first{% endif %}">
        <h1 class="title">
            <a href="{{ child.url }}">{{ child.title or url }}</a>
            <ul class="meta">
                {% if child.published %}
                <li>Опубликовано: {{ child.published.strftime('%d.%m.%Y') }}</li>
                {% endif %}
                <li><a href="{{ github }}{{ child.index_file or child.url }}">смотреть на github</a></li>
            </ul>
        </h1>
        {{ child.summary }}
    </li>
{% endfor %}
</ul>
{% endblock%}
