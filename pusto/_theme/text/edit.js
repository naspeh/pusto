$(document).ready(function() {
    var container = $('#text-edit');
    var reset = $('#action-reset');

    var need_save = function() {
        if ($('#editor').hasClass('changed') && !confirm('Кусок не сохранен, продолжить?')) {
            $('#editor textarea').focus();
            return true;
        }
        $('#editor').removeClass('changed');
        return false;
    }

    container.live('start-loading', function() {
        container.find('.loading').show();
    });
    container.live('stop-loading', function() {
        container.find('.loading').hide();
    });

    container.live('init', function() {
        var choicer = $('#bit-choicer');
        var editor = $('#text-edit');
        var url = editor.find('#text-url').val();
        if (url != window.location.pathname) {
            window.location = url;
        }

        var active = editor.find('.bit.active');
        window.location.hash = ''
        window.location.hash = active.attr('id');

        var insert = $('#bit-insert');
        if (insert.length > 0) {
            insert.change();
            //choicer.focus();
        }
        editor.find('#editor textarea').focus();
        return false;
    });

    $('#bit-choicer').live('change', function() {
        if (need_save()) {
            var active = $('#viewer .bit.active');
            var choice = $(this).find('option:[value=' + active.attr("name") + ']');
            choice.attr('selected', 'selected');
            return false;
        }
        reset.click();
    });

    $('#toolbar a.edit, #toolbar a.preview, #toolbar a.src, #toolbar a.html').live('click', function() {
        if (need_save()) {
            return false;
        }
        var $this = $(this);
        container.trigger('start-loading');
        if ($this.hasClass('edit')) {
            reset.click();
            return false
        }

        var toolbar = $this.parent();
        var viewer = container.find('#viewer');
        var editor = container.find('#editor');
        var href = $this.attr('href').replace('#', '');
        toolbar.find('.options').removeClass('active');
        container.find('#options').hide();
        if ($this.hasClass('preview')) {
            editor.hide();
        } else if ($this.hasClass('src') || $this.hasClass('html')) {
            editor.show();
        }
        $this.after(toolbar.find('a.edit'));
        toolbar.find('a').show();
        $this.hide();
        $.post(href, function(data) {
            viewer.html(data);
            container.trigger('stop-loading');
        });
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
                if (div.find('.errors').length == 0) {
                    reset.click();
                }
            }
        });
        return false;
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
                container.trigger('start-loading');
            },
            'success': function(data, status) {
                var editor = $('#text-edit');
                editor.html($(data).html());
                container.trigger('init');
                container.trigger('stop-loading');
           }
        });
        return false;
    });

    $('#viewer .bit .info').live('click', function() {
        if (need_save()) {
            return false;
        }
        var choicer = $('#bit-choicer');
        var bit = $(this).parent();
        bit = bit.attr('name');
        var choice = choicer.find('option:[value=' + bit + ']');
        choice.attr('selected', 'selected');
        choicer.change();
        return false;
    });

    $('#bit-insert').live('change', function() {
        var $this = $(this);
        var parent = $('#bit-parent');
        if (parent.find('option').length) {
            parent.show();
            $this.show();
        } else {
            parent.hide();
            $this.hide();
        }
        var selected = $this.find(':selected');
        if (selected.val() == '') {
            parent.hide();
        }
    });

    // Styles
    $('#editor textarea').tabOverride().live({
        'change': function() {
            $('#editor').addClass('changed');
        },
        'focus': function() {
            $(this).parents('.textarea').addClass('active');

        },
        'blur': function() {
            $(this).parents('.textarea').removeClass('active');
        }
    });

    // Initial page
    container.trigger('init');
    $.fn.tabOverride.setTabSize(4);
});
