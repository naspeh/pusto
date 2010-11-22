$(document).ready(function() {
    var reset = $('#action-reset');

    reset.live('click', function() {
        var choicer = $('#bit-choicer');
        var editor = $('.b-wrap');
        editor.find('.bit').removeClass('active');

        var selected = choicer.find(':selected').html();
        var bit = editor.find('#bit-' + selected.replace('#', ''));
        bit.addClass('active')
        window.location.hash = '#' + bit.attr('name');

        var insert = $('#bit-insert');
        insert.find('option[value=""]').attr('selected', 'selected');
        insert.change();

        choicer.focus();
        return false;
    });
    reset.click();

    $('#bit-choicer').live('change', function() {
        reset.click();
    });

    $('#action-apply, #action-delete, #action-reset').live('click', function() {
        var form = $('#editor-form');
        var selected = form.find(':selected');
        var action = $(this).attr('value');
        if (action == 'delete' &&  !confirm('Точно хотите удалить ' + selected.html() + '?')) {
            return false;
        }
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
    $('.b-viewer .bit .info').live('click', function() {
        var choicer = $('#bit-choicer');
        var bit = $(this).parent();
        bit = bit.attr('name').replace('bit-', '');
        var choice = choicer.find('option:contains(#' + bit + ')');
        choice.attr('selected', 'selected');
        reset.click();
        return false;
    });
    $('#bit-insert').live('change', function() {
        var $this = $(this);
        var choicer = $('#bit-choicer');
        var parent = $('#bit-parent');
        var selected = $this.find(':selected');
        var bit_selected = choicer.find(':selected');
        if (selected.val() == '') {
            parent.hide();
            return;
        }

        var options = choicer.find('option').clone();
        parent.html(options);
        parent.find('option[value="new"]').remove();
        parent.find('option[value="' + bit_selected.val() + '"]').remove();
        parent.show();
    });
});
