{% extends '_theme/list.tpl' %}
{% set children=children['/post/'].children %}

{% block body %}
<!--META{
    "aliases": ["/post/"]
}-->
{{ super() }}
{% endblock %}
