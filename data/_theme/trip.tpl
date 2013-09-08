{% extends '_theme/base.tpl' %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
{% endblock %}

{% block meta %}
    <li><a href="/trip/">наверх</a></li>
    {{ super() }}
{% endblock %}
