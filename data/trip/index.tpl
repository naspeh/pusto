{% extends '_theme/base.tpl' %}
{% from '_theme/macros.tpl' import show_children %}

{% set title="Отчеты о наших поездках" %}
{% block title %}{{ title }}{% endblock %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
    <script>
    $(document).ready(function() {
        $.fn.napokaz.defaults.set({
            boxThumbsize: '100c',
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
<div class="intro">
    <h1>{{ title }}</h1>
    {{ intro() }}
</div>

{{ show_children(children) }}
{% endblock %}
