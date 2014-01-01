{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% block head %}
    {{ super() }}

    {% if p.params and p.params.feed %}
    <link
        href="{{ p.params.feed }}" rel="alternate"
        type="application/atom+xml" title="{{ p.title | striptags }}"
    />
    {% endif %}
{% endblock %}

{% block body %}
<div class="intro">
    <h1>{{ p.title }}</h1>
    {{ p.body }}
</div>

{{ show_children(p.children) }}
{% endblock %}
