$(document).ready(function() {
    var reset = $('#action-reset');

    reset.live('click', function() {
        var choicer = $('#bit-choicer');
        var editor = $('.b-wrap');
        editor.find('.bit').removeClass('active');

        var selected = choicer.find(':selected').html();
        var bit = editor.find('#bit-' + selected.replace('#', ''));
        bit.addClass('active')
        window.location.hash = '#' + bit.attr('id');

        var insert = $('#bit-insert');
        insert.find('option[value=""]').attr('selected', 'selected');
        insert.change();

        if (selected=='#new') {
            editor.find('#action-delete').hide();
        } else {
            editor.find('#action-delete').show();
        }

        choicer.focus();
        return false;
    });

    $('#bit-choicer').live('change', function() {
        reset.click();
    });

    $('.b-toolbar a').live('click', function() {
        var $this = $(this);
        var toolbar = $this.parent();
        var editor = $('.b-wrap');
        if ($this.hasClass('fixsize')) {
            editor.find('.b-preview').hide().html('');
            editor.find('.b-viewer, .b-editor').show();
            $this.hide();
            toolbar.find('.fluidsize').show();
        } else if ($this.hasClass('fluidsize')) {
            var viewer = editor.find('.b-preview');
            editor.find('.document').clone().appendTo(viewer);
            viewer.show()
            editor.find('.b-viewer, .b-editor').hide();
            $this.hide();
            toolbar.find('.fixsize').show();
        } else if ($this.hasClass('delete') && confirm('Точно хотите удалить?')) {
            var href = $this.attr('href').replace('#', '');
            $this.attr('href', href);
        }
    })

    $('#action-apply, #action-delete, #action-reset').live('click', function() {
        var form = $('#editor-form');
        var url = form.find('#text-url').val();
        var selected = form.find(':selected');
        var action = $(this).attr('value');
        if (action == 'delete' &&  !confirm('Точно хотите удалить ' + selected.html() + '?')) {
            return false;
        }
        form.ajaxSubmit({
            'data': {action: action},
            'beforeSubmit': function() {
                $('.b-wrap').find(':input').attr('disabled', 'disabled');
            },
            'success': function(data, status) {
                var editor = $('.b-wrap');
                if (action=='reset') {
                    editor.find('textarea').val(data);
                } else {
                    editor.html(data);
                    var new_url = editor.find('#text-url').val();
                    if (url != new_url) {
                        window.location = new_url;
                    }
                    reset.click();
                }
                editor.find(':input').attr('disabled', '');
           }
        });
        return false;
    });
    $('.b-viewer .bit .info').live('click', function() {
        var choicer = $('#bit-choicer');
        var bit = $(this).parent();
        bit = bit.attr('name');
        var choice = choicer.find('option:[value="' + bit + '"]');
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
        var options = choicer.find('option').clone();
        parent.html(options);
        parent.find('option[value="new"]').remove();
        parent.find('option[value="' + bit_selected.val() + '"]').remove();
        if (parent.find('option').length) {
            parent.show();
            $this.show();
        } else {
            parent.hide();
            $this.hide();
        }
        if (selected.val() == '') {
            parent.hide();
        }
    });

    // Initial page
    reset.click();
});
