napokaz.js
==========
.. note:: `Google closed Picasa Web Albums at May 1, 2016.`__

    *So this viewer is outdated, though examples are still working.*

__ http://googlephotos.blogspot.com/2016/02/moving-on-from-picasa.html

| Lightweight viewer for images from `picasaweb.`__
| Source code available on `github.`__

__ https://picasa.google.com/
__ https://github.com/naspeh/napokaz

.. compound::
    Example of usage
        .. code:: html

            <!-- Put to head -->
            <link rel="stylesheet" href="napokaz.css" />

            <!-- Put to body -->
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

            <!-- Put to end of body -->
            <script src="http://code.jquery.com/jquery.js"></script>
            <script src="napokaz.js"></script>
            <script>
                $('.napokaz').napokaz();
            </script>

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
