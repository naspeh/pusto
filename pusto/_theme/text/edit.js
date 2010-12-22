$(document).ready(function() {
    var reset = $('#action-reset');

    reset.live('click', function() {
        var choicer = $('#bit-choicer');
        var editor = $('#text-edit');
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
        if (choicer.find('option').length > 1) {
            choicer.focus();
        } else {
            editor.find('textarea').focus();
        }
        return false;
    });

    $('#bit-choicer').live('change', function() {
        reset.click();
    });

    $('#toolbar a.edit, #toolbar a.preview').live('click', function() {
        var $this = $(this);
        var toolbar = $this.parent();
        var editor = $('#text-edit');
        if ($this.hasClass('edit')) {
            editor.find('#preview').hide().html('');
            editor.find('#viewer, #editor').show();
            $this.hide();
            toolbar.find('.preview').show();
        } else if ($this.hasClass('preview')) {
            var viewer = editor.find('#preview');
            viewer.load("{{ app.url_for(':text.show', id=text._id) }}").show();
            editor.find('#viewer, #editor').hide();
            $this.hide();
            toolbar.find('.edit').show();
        }
        return false;
    });

    $('#toolbar a.delete').live('click', function(){
        var $this = $(this);
        if (confirm('Точно хотите удалить?')) {
            var href = $this.attr('href').replace('#', '');
            $this.attr('href', href);
        }
    });

    $('#toolbar a.options').live('click', function(){
        var $this = $(this);
        var div = $("#options");
        if ($this.hasClass('active')) {
            div.slideUp();
            $this.removeClass('active');
        } else {
            $this.addClass('active');
            var url = div.find('form').attr('action');
            url += '?content=' + div.find('input[name="content"]').val();
            $.get(url, function(data){
                div.html(data);
                div.slideDown();
                div.find(':text:first').focus();
            });
        }
        return false
    });

    $('#options form').live('submit', function(){
        var $this = $(this);
        $this.ajaxSubmit({
            'beforeSubmit': function() {
                $('#options').find(':input').attr('disabled', 'disabled');
            },
            'success' : function(data) {
                var div = $('#options');
                div.html(data);
                div.find(':input').attr('disabled', '');
            }
        });
        return false;
    });

    $('#action-apply, #action-delete, #action-reset').live('click', function() {
        var form = $('#editor-form');
        var url = window.location.pathname;
        var selected = form.find(':selected');
        var action = $(this).attr('value');
        if (action == 'delete' &&  !confirm('Точно хотите удалить ' + selected.html() + '?')) {
            return false;
        }
        form.ajaxSubmit({
            'data': {action: action},
            'beforeSubmit': function() {
                $('#text-edit').find(':input').attr('disabled', 'disabled');
            },
            'success': function(data, status) {
                var editor = $('#text-edit');
                if (action=='reset') {
                    editor.find('textarea').val(data);
                } else {
                    editor.html($(data).html());
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

    $('#viewer .bit .info').live('click', function() {
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
