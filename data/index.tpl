{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% set title='Гриша aka naspeh' %}
{% block title %}{{ title }}{% endblock %}

{% macro intro() %}
{% filter rst %}

Статьи о **python, linux, web**

{% endfilter %}
{% endmacro %}

{% block body %}
<!--META{
    "aliases": ["/post/"]
}-->

<div class="title">
    <h1>{{ title }}</h1>
    <div class="intro">{{ intro() }}</div>
</div>
{{ show_children(children['/post/'].children) }}

{% endblock %}
