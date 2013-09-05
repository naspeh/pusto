{% extends '_theme/list.tpl' %}
{% set children=children['/post/'].children %}
{% block title%}Гриша aka naspeh{% endblock %}
{% block body %}
<!--META{
    "aliases": ["/post/"]
}-->
{{ super() }}
{% endblock %}
