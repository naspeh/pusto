@import url(http://fonts.googleapis.com/css?family=PT+Sans:400,700,400italic,700italic&subset=latin,cyrillic);
@import url(http://fonts.googleapis.com/css?family=Philosopher:700&subset=latin,cyrillic);
@import url(http://fonts.googleapis.com/css?family=Anonymous+Pro:400,400italic,700,700italic&subset=latin,cyrillic);

{{ load_file('_theme/reset.css', '_theme/syntax.css') }}

/* Init qTip2 */
{{ load_file('_theme/libs/jquery.qtip.min.css') }}
.qtip {
    font-size: 12px;
    line-height: 14px;
}

/* Init napokaz */
{{ load_file('s/napokaz/src/napokaz.css') }}
.napokaz, .napokaz-term {
    display: inline-block;
    *display: inline;
    *zoom: 1;
    margin: 0 5px;
    margin-bottom: 1em;
    vertical-align: top;
}
{{ load_file('_theme/styles.css') }}
