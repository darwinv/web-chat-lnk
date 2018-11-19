
$(function() {
    $(document).ready(function() {
    });

    $('#accept-button').click(function(event) {
        $('#thanks-for-payment-modal').modal('hide');
    });

    $('#thanks-for-payment-modal').on('hidden.bs.modal', function () {
        window.location.replace(redirect_to);
    })
});
