{% extends "_theme/base.tpl" %}
{% block title %}napokaz{% endblock %}

{% set repo="https://rawgithub.com/naspeh/napokaz/master/"%}
{% block head_extra %}
    <link rel="stylesheet" href="{{ repo }}napokaz.css" />

    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="{{ repo }}napokaz.js"></script>
    <script>
        $(document).ready(function() {
            $('.napokaz').napokaz();
        });
    </script>
    <style>
        .napokaz {
            display: inline-block;
            *display: inline;
            *zoom: 1;
            margin: 5px;
            vertical-align: top;
        }
    </style>
{% endblock %}

{% block body %}
    <div class="napokaz"
        data-box-thumbsize='72u'
        data-front-thumbsize='40u'>
    </div>
    <div class="napokaz"
        data-box-thumbsize='90c'
        data-front-thumbsize='60c'>
    </div>

    <div class="napokaz"
        data-picasa-album="ProfilePhotos">
    </div>
    <div>
        <div class="napokaz"
            data-box-width="6"
            data-picasa-filter="we"
            data-picasa-album="ScrapbookPhotos">
        </div>
        <div class="napokaz"
            data-box-width="6"
            data-picasa-filter="we"
            data-picasa-ignore="hide"
            data-picasa-album="ScrapbookPhotos">
        </div>
        <div class="napokaz"
            data-box-width="6"
            data-picasa-ignore="we"
            data-picasa-album="ScrapbookPhotos">
        </div>
    </div>

    <div class="napokaz"
        data-front-thumbsize="60c"
        data-box-thumbsize="120c"
        data-picasa-album="20121016_Karpaty_Spravzhnya_Kazka">
    </div>
{% endblock %}
