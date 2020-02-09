{% extends '_theme/photos.tpl' %}

{% block body %}
{{ super() }}
<div id="gallery">
{% for i in p.photos %}
<a data-fancybox="photo" href="{{ i.src }}"><img src="{{ i.thumb }}"/></a>
{% endfor %}
</div>
{% endblock %}
