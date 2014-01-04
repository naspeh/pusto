{% extends '_theme/list.tpl' %}

{% block js %}
    {{ super() }}
    <script>
    $(document).ready(function() {
        $('.napokaz').napokaz();
    });
    </script>
{% endblock %}
