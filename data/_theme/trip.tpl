{% extends '_theme/base.tpl' %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
    <script>
    $(document).ready(function() {
        $.fn.napokaz.defaults.set({
            frontCount: 10,
            frontThumbsize: '60c',
            picasaIgnore: 'hide'
        });
        $('.napokaz').napokaz();
    });
    </script>
{% endblock %}
