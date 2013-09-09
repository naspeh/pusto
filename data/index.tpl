{% extends '_theme/base.tpl' %}
{% block title%}Гриша aka naspeh{% endblock %}
{% block body %}
<!--META{
    "aliases": ["/post/"]
}-->
{% set children=children['/post/'].children %}
{% include '_theme/list.tpl' with context %}
{% endblock %}
