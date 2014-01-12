napokaz.js
----------
.. code:: html

    <!-- Example of usage -->
    <script src="http://code.jquery.com/jquery.js"></script>

    <link rel="stylesheet" href="napokaz.css" />
    <script src="napokaz.js"></script>
    <script>
        $(document).ready(function() {
            $('.napokaz').napokaz();
        });
    </script>

    <div class="napokaz"
        data-box-thumbsize="120c"
        data-front-thumbsize="60c"
        data-picasa-user="naspeh"
        data-picasa-album="20121016_Karpaty_Spravzhnya_Kazka">
    </div>
    <div class="napokaz"
        data-picasa-user="naspeh"
        data-picasa-albumid="5486642664135948337">
    </div>

data-picasa-albumid
    .. raw:: html

        <div class="napokaz"
            data-picasa-albumid="5486642664135948337">
        </div>
        <div class="napokaz"
            data-picasa-albumid="5220591610866623377">
        </div>

data-box-width & data-box-height
    .. raw:: html

        <div class="napokaz"
            data-box-width="3"
            data-box-height="2"

            data-box-thumbsize='60c'>
        </div>
        <div class="napokaz"
            data-box-width="1"

            data-box-thumbsize='60c'>
        </div>
        <div class="napokaz"
            data-box-width="1"
            data-box-height="6"

            data-box-thumbsize='60c'>
        </div>

data-picasa-filter & data-picasa-ignore
    .. raw:: html

        <div class="napokaz"
            data-picasa-ignore="we"

            data-box-width="4"
            data-box-thumbsize='60c'
            data-picasa-album="Naspeh">
        </div>
        <div class="napokaz"
            data-picasa-filter="velo"

            data-box-width="4"
            data-box-thumbsize='60c'
            data-picasa-album="Naspeh">
        </div>
        <div class="napokaz"
            data-picasa-filter="we"
            data-picasa-ignore="naspeh, velo"

            data-box-width="4"
            data-box-thumbsize='60c'
            data-picasa-album="Naspeh">
        </div>

data-box-thumbsize & data-front-thumbsize
    .. raw:: html

        <div class="napokaz"
            data-box-thumbsize='80u'
            data-front-thumbsize='40u'>
        </div>
        <div class="napokaz"
            data-box-thumbsize='120c'
            data-front-thumbsize='60c'>
        </div>
        <div class="napokaz"
            data-box-thumbsize="160c"
            data-front-thumbsize="80c"
            data-picasa-album="20121016_Karpaty_Spravzhnya_Kazka">
        </div>
