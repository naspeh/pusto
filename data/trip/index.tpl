{% extends '_theme/base.tpl' %}

{% set title="Отчеты о наших поездках" %}
{% block title %}{{ title }}{% endblock %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
    <script>
    $(document).ready(function() {
        $.fn.napokaz.defaults.set({
            frontCount: 10,
            frontThumbsize: '60c',
            frontUseHash: false,
            picasaIgnore: 'hide'
        });
        $('.napokaz').napokaz();
    });
    </script>
{% endblock %}

{% macro intro() %}
{% filter rst %}

**Авторы:** Гриша и Катя Костюк

{% endfilter %}
{% endmacro %}

{% block body %}
<div class="title">
    <h1>{{ title }}</h1>
    <div class="intro">{{ intro() }}</div>
</div>

{% include '_theme/list.tpl' %}
{% endblock %}
