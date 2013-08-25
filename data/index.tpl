{% extends '_theme/base.tpl' %}
{% block body %}
<ul>
{% for url in meta.child_urls %}
    <li><a href="{{ url }}">{{ url }}</a></li>
{% endfor %}
</ul>
{% endblock%}
