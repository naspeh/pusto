{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% set title='Статьи о python, linux, web' %}
{% block title %}{{ title }}{% endblock %}

{% macro intro() %}
{% filter rst %}

**Автор:** Гриша Костюк

{% endfilter %}
{% endmacro %}

{% block body %}
<!--
META{
    "aliases": ["/post/", "/s/"]
}
-->

<div class="intro">
    <h1>{{ title }}</h1>
    {{ intro() }}
</div>

{{ show_children(children['/post/'].children) }}
{% endblock %}
