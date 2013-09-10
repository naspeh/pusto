{% extends '_theme/base.tpl' %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
    <script>
        $.fn.napokaz.defaults.frontUseHash = false;
        $('.napokaz').napokaz();
    </script>
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
