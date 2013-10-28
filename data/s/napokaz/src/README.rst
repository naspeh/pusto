Lightweight image viewer for picasaweb__
----------------------------------------

__ https://picasaweb.google.com/

Has one dependence jquery. Formally jquery plugin.

`Live examples. <http://pusto.org/s/napokaz/>`_

Usage:

.. code:: html

    <link rel="stylesheet" href="napokaz.css" />
    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="napokaz.js"></script>
    <script>
        $(document).ready(function() {
            $('.napokaz').napokaz();
        });
    </script>

    <div class="napokaz"
        data-front-thumbsize="60c"
        data-box-thumbsize="120c"
        data-picasa-album="20121016_Karpaty_Spravzhnya_Kazka">
    </div>
    <div class="napokaz"
        data-picasa-user="115954385615646692819"
        data-picasa-albumid="5923049200824375969">
    </div>

**Screenshot:**

.. image:: screenshot.png
