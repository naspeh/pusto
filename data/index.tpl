{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}
{% block title%}Гриша aka naspeh{% endblock %}
{% block body %}
<!--META{
    "aliases": ["/post/"]
}-->
{{ show_children(children['/post/'].children) }}
{% endblock %}
