{% from '_theme/macros.tpl' import show_meta %}
<!DOCTYPE HTML>
{% set EN = p.params.lang == 'en' %}
<head>
{% block head %}
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/all.css?{{ p.pages['/all.css'].mtime }}" type="text/css" />
    <title>pusto.org: {% block title %}{{ p.title|striptags or p.url }}{% endblock %}</title>
{% endblock %}
</head>

<body>
{% block header %}
{% if EN %}
<div class="header">
    <a class="logo" href="/en/">pusto.org</a>
    <ul class="nav">
        <li><a href="/en/resume/">CV</a></li>
        <li><a href="/">Articles (Ru)</a></li>
        <li><a href="/trip/">Trips (Ru)</a></li>
    </ul>
</div>
{% else %}
<div class="header">
    <a class="logo" href="/">pusto.org</a>
    <ul class="nav">
        <li><a href="/trip/">Наши поездки</a></li>
        <li><a href="/naspeh/">Об авторе</a></li>
    </ul>
</div>
{% endif %}
{% endblock %}


{% block body %}
<div itemscope="itemscope" itemtype="http://schema.org/Article">
    {% if p.title %}
    <div class="title">
        <h1 itemprop="name">{{ p.title }}</h1>
        <link itemprop="url" href="{{ url }}" />
        {{ show_meta(p, back_url=True, EN=EN)}}
    </div>
    {% endif %}
    <div class="document">
        {% block document %}
        {{ p.body }}
        {% endblock%}
    </div>
    {% if p.terms %}
    <hr />
    <div class="terms" id="terms">
        <h3 class="terms-title"><a href="#terms">{{ p.terms.title }}</a></h3>
        <div class="terms-body group">
            {{ p.terms.body }}
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block js %}
<script src="/all.js?{{ p.pages['/all.js'].mtime }}"></script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-6254112-1', 'pusto.org');
  ga('send', 'pageview');
</script>
{% endblock %}
</body>
