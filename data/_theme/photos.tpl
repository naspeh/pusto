{% extends '_theme/base.tpl' %}

{% block head %}
    {{ super() }}
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/justifiedGallery@3.7.0/dist/css/justifiedGallery.css"/>
{% endblock %}

{% block js %}
    {{ super() }}
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.4.1/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@fancyapps/fancybox@3.5.7/dist/jquery.fancybox.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/justifiedGallery@3.7.0/dist/js/jquery.justifiedGallery.min.js"></script>
    <script>
    $("#gallery").justifiedGallery({
        rowHeight : 150,
        // margins : 3,
        // lastRow : 'nojustify',
    });
    </script>
{% endblock %}

{% block body %}
    <div class="title">
        <ul class="meta">
            <li><a href="{{ p.parent.parent.url }}">{{ p.parent.parent.title|striptags }}</a></li>
            <li><a href="{{ p.parent.url }}">{{ p.parent.title|striptags }}</a></li>
        </ul>
    </div>
{% endblock %}
