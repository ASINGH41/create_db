$(function() {
    $('input[name="is_delivery"]').on('click', function() {
        if ($(this).val() == '1') {
            $('#address').show();
        }
        else {
            $('#address').hide();
        }
    });
});