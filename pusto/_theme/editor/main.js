$(document).ready(function() {
    $('#editor-form button[type=submit]').live('click', function() {
        var form = $('#editor-form');
        var selected = form.find(':selected').val();
        form.ajaxSubmit({
            'data': {'action': $(this).attr('value')},
            'beforeSubmit': function() {
                var editor = $('.b-wrap');
                editor.find('input, textarea, select').attr('disabled', 'disabled');
            },
            'success': function(data, status) {
                var editor = $('.b-wrap');
                update(editor, data);
           }
        });
        return false;
    });

    $('#bit-choicer').live('change', function() {
        var editor = $('.b-wrap');
        var selected = $(this).find(':selected').val();
        var url = '{{ app.url_for(":editor.bit_src", id="ID") }}'.replace('ID', selected)
        //editor.find('input, textarea, select').attr('disabled', 'disabled');
        $.get(url, function(data) {
            update(editor, data);
            editor.find('input, textarea, select').attr('disabled', '');
        });
    });

    activate($('.b-wrap'));

    function activate(editor) {
        var selected = $('#bit-choicer').find(':selected').html();
        var bit = editor.find('#bit-' + selected.replace('#', ''));
        window.location.hash = '#' + bit.attr('name');
        bit.addClass('active')
    }

    function update(editor, data) {
        editor.html(data);
        editor.find('input, textarea, select').attr('disabled', '');
        activate(editor);
    }
});
