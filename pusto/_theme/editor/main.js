$(document).ready(function() {
    var reset = $('#action-reset');
    reset.live('click', function() {
        var editor = $('.b-wrap');
        editor.find('.bit').removeClass('active');
        var selected = $('#bit-choicer').find(':selected').html();
        var bit = editor.find('#bit-' + selected.replace('#', ''));
        bit.addClass('active')
        window.location.hash = '#' + bit.attr('name');
        $('#bit-choicer').focus();
        return false;
    });
    $('#action-apply, #action-delete, #action-reset').live('click', function() {
        var form = $('#editor-form');
        var selected = form.find(':selected').val();
        var action = $(this).attr('value'); 
        form.ajaxSubmit({
            'data': {action: action},
            'beforeSubmit': function() {
                $('.b-wrap').find('input, textarea, select').attr('disabled', 'disabled');
            },
            'success': function(data, status) {
                var editor = $('.b-wrap');
                if (action=='reset') {
                    editor.find('textarea').val(data);
                    editor.find('input, textarea, select').attr('disabled', '');
                } else {
                    editor.html(data);
                    editor.find('input, textarea, select').attr('disabled', '');
                    reset.click();
                }
           }
        });
        return false;
    });
    $('#bit-choicer').live('change', function() {
        reset.click();
    });
    $('.b-viewer .bit .info').live('click', function() {
        var bit = $(this).parent();
        bit = bit.attr('name').replace('bit-', '');
        var choice = $('#bit-choicer').find('option:contains(#' + bit + ')');
        choice.attr('selected', 'selected');
        reset.click();
        return false;
    });
    reset.click();
});
