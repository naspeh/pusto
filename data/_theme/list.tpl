{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% block head %}
    {{ super() }}

    {% if params.feed %}
    <link
        href="{{ params.feed }}" rel="alternate"
        type="application/atom+xml" title="{{ title | striptags }}"
    />
    {% endif %}
{% endblock %}

{% block body %}
<div class="intro">
    <h1>{{ title }}</h1>
    {{ body }}
</div>

{% if params.root %}{% set children=pages[params.root].children %}{% endif %}
{{ show_children(children) }}
{% endblock %}
