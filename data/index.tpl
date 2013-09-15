{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% set title='Гриша aka naspeh. Статьи о python, linux, web' %}
{% block title %}{{ title }}{% endblock %}

{% block body %}
<!--META{
    "aliases": ["/post/"]
}-->

<div class="intro">
    <h1>{{ title }}</h1>
</div>
{{ show_children(children['/post/'].children) }}

{% endblock %}
