{% extends '_theme/base.tpl' %}

{% block js %}
    {{ super() }}
    <script>
    $(document).ready(function() {
        $.fn.napokaz.defaults.set({
            boxThumbsize: '100c',
            frontCount: 10,
            frontThumbsize: '60c',
            frontUseHash: true,
            picasaIgnore: 'hide'
        });
        $('.napokaz').napokaz();
    });
    </script>
{% endblock %}
