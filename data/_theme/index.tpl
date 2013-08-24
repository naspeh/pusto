<!DOCTYPE HTML>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/_theme/reset.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/styles.css" type="text/css" />
    <link rel="stylesheet" href="/_theme/syntax.css" type="text/css" />
    <title>pusto.org: {{ title or url }}</title>
</head>
<body>
    {% if html_title %}
    <h1 class="title">
        {{ html_title }}
        {% if created %}
        <div class="title-created" title="Опубликовано: {{ created }}">
            {{ created }}
        </div>
        {% endif %}
    </h1>
    {% endif %}
    {{ html_body }}
</body>
