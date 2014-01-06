{% set github="https://github.com/naspeh/pusto/tree/master/data" %}

{% macro show_meta(c, back_url=False) %}
<ul class="meta">
    {% if back_url %}
        {% if c.parent.url == '/post/' %}
        <li><a href="/">{{ c.parent.title|striptags }}</a></li>
        {% elif c.parent %}
        <li><a href="{{ c.parent.url }}">{{ c.parent.title|striptags }}</a></li>
        {% endif %}
    {% endif %}
    {% if c.author %}
    <li>
        {% if c.author|length == 1 %}
        Автор: <b>{{ c.author[0] }}</b>
        {% else %}
        Авторы: <b>{{ ', '.join(c.author)}}</b>
        {% endif %}
    </li>
    {% endif %}
    {% if c.published %}
    <li itemprop="datePublished" datetime="{{ c.published.strftime('%Y-%m-%d')}}" >
        Опубликовано: <b>{{ c.published.strftime('%d.%m.%Y') }}</b>
    </li>
    {% endif %}
    {% if c.type in ['md', 'rst'] %}
    <li><a href="{{ c.index_file }}">исходный текст</a></li>
    {% endif %}
    <li><a href="{{ github }}{{ c.url }}">Смотреть на github</a></li>
</ul>
{% endmacro %}

{% macro show_children(children) %}
<ul class="posts">
{% for url, child in children.items() %}
    <li class="post" itemscope="itemscope" itemtype="http://schema.org/Article">
        <div class="title">
            <h1 itemprop="name">
                <a href="{{ child.url }}" itemprop="url">
                    {{ child.title|striptags or url }}
                </a>
            </h1>
            {{ show_meta(child) }}
        </div>
        {% if child.summary %}
        <div itemprop="description">
            {{ child.summary }}
        </div>
        {% endif %}
    </li>
{% endfor %}
</ul>
{% endmacro %}
