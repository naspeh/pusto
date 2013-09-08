{% set repo="https://rawgithub.com/naspeh/napokaz/master/"%}
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
        margin: 0 5px;
        margin-bottom: 1em;
        vertical-align: top;
    }
</style>
