// Run once the document has loaded
$(document).ready(function() {
    $('#button').click(function() {
        var input = $(this).data('action');
        $.ajax({
            url: '/candyland/',
            type: 'POST',
            data: {'button': input},
        });
    });
});