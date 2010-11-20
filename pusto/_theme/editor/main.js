$(document).ready(function() {
    $('#editor-form').ajaxForm({
        'success': function(data, status) {
            console.debug(status);
            var viewer = $('.b-viewer');
            viewer.html(data);
            var active = viewer.find('.bit.last')
            if (active.length==1) {
                window.location.hash = '#' + active.attr('name');
            }
        }
    });
});
