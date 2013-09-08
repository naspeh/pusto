{% extends '_theme/base.tpl' %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
{% endblock %}

{% block document %}
    {{ super() }}
{% endblock %}
