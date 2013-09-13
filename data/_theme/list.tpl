<ul class="posts">
{% for url, child in children.items() %}
    <li class="{% if loop.index == 1 %}post-first {% endif %}post" itemscope="itemscope" itemtype="http://schema.org/Article">
        <div class="title">
            <h1 itemprop="name">
                <a href="{{ child.url }}" itemprop="url">
                    {{ child.title|striptags or url }}
                </a>
            </h1>
            <ul class="meta">
                {% if child.published %}
                <li itemprop="datePublished" datetime="{{ child.published.strftime('%Y-%m-%d')}}" >
                    Опубликовано: {{ child.published.strftime('%d.%m.%Y') }}
                </li>
                {% endif %}
                {% if child.author %}
                <li>
                    автор:
                    {% if child.author == 'nayavu' %}
                        Катя
                    {% elif child.author == 'naspeh' %}
                        Гриша
                    {% endif %}
                </li>
                {% endif %}
                {% if child.markup in ['md', 'rst'] %}
                <li><a href="{{ child.index_file }}">{{ child.markup }} текст</a></li>
                {% endif %}
                <li><a href="{{ github }}{{ child.index_file or child.url }}">смотреть на github</a></li>
            </ul>
        </div>
        {% if child.summary %}
        <div itemprop="description">
            {{ child.summary }}
        </div>
        {% endif %}
    </li>
{% endfor %}
</ul>
