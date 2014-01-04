{% extends '_theme/base.tpl' %}

{% set napokaz_skip=True %}
{% block head %}
    {{ super() }}
    <script>
    $(document).ready(function() {
        $.fn.napokaz.defaults.set({
            boxThumbsize: '100c',
            frontCount: 10,
            frontThumbsize: '60c',
            picasaIgnore: 'hide'
        });
        $('.napokaz').napokaz();
    });
    </script>
{% endblock %}
