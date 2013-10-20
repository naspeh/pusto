{% extends '_theme/list.tpl' %}

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
