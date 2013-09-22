{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% set title='Черновики' %}
{% block title %}{{ title }}{% endblock %}

{% block body %}
<div class="intro">
    <h1>{{ title }}</h1>
</div>

{{ show_children(children) }}
{% endblock %}
