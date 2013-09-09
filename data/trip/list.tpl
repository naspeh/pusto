{% extends '_theme/base.tpl' %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
    <style type="text/css">
    #about {
        border-bottom: 1px solid #777;
        margin-bottom: 1em;
    }
    </style>
{% endblock %}

{% block body %}
<div class="title">
    <h1>{{ title }}</h1>
    <div class="intro">
        {{ body }}
    </div>
</div>

{% include '_theme/list.tpl' %}
{% endblock %}
