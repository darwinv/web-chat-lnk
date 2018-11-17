
$(function() {
    const HTTP_CODES = {OK:"200", CREATED:"201", BAD_REQUEST:"400", NOT_FOUND:"404"}

    $(document).ready(function() {
    });

    $('#upload-button').click(function(event) {
        $('#upload-voucher-modal').modal('show');
    });
});