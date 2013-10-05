{% extends '_theme/base.tpl' %}
{% block title %}napokaz{% endblock %}

{% block head %}
    {{ super() }}
    {% include '_theme/napokaz.tpl' %}
    <script>
    $(document).ready(function() {
        $.fn.napokaz.defaults.set({
            frontCount: 10,
            frontThumbsize: '60c'
        });
        $('.napokaz').napokaz();
    });
i   </script>
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
        data-picasa-user="115954385615646692819"
        data-picasa-albumid="5923049200824375969">
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
    <div>
        <div class="napokaz"
            data-box-width="3"
            data-box-height="2">
        </div>
        <div class="napokaz"
            data-box-width="1"
            data-box-height="6">
        </div>
    </div>
    <div>
        <div class="napokaz"
            data-picasa-user="115954385615646692819"
            data-picasa-albumid="5220591610866623377">
        </div>
    </div>
{% endblock %}
