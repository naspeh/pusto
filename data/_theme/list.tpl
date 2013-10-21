{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% block body %}
<div class="intro">
    <h1>{{ title }}</h1>
    {{ body }}
</div>

{% if children_path %}
    {% set children=pages[children_path].children %}
{% endif %}

{{ show_children(children) }}
{% endblock %}
