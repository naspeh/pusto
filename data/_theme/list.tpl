{% extends '_theme/base.tpl' %}
{% block body %}
<ul class="posts">
{% for url, child in children.items() %}
    <li class="{% if loop.index == 1 %}post-first {% endif %}post">
        <div class="title">
            <h1><a href="{{ child.url }}">{{ child.title|striptags or url }}</a></h1>
            <ul class="meta">
                {% if child.published %}
                <li>Опубликовано: {{ child.published.strftime('%d.%m.%Y') }}</li>
                {% endif %}
                <li><a href="{{ github }}{{ child.index_file or child.url }}">смотреть на github</a></li>
            </ul>
        </div>
        {% if child.summary %}{{ child.summary }}{% endif %}
    </li>
{% endfor %}
</ul>
{% endblock%}
