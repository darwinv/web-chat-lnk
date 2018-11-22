
$(function() {
    const HTTP_CODES = {OK:200, CREATED:201, BAD_REQUEST:400, NOT_FOUND:404}

    $(document).ready(function() {
        $('#send-button').prop('disabled', true);
    });

    $('#voucher-section').click(function(event) {
        $('#file-input').trigger('click');
    });

    $('#file-input').change(function(event) {
        var file = $('#file-input').prop('files')[0];
        if (file == null || file == "") {
            return;
        }

        var preview = $('#voucher-img')
        var reader  = new FileReader();

        reader.onloadend = function () {
           preview.attr('src', reader.result);
           $('#send-button').prop('disabled', false);
        }

        reader.readAsDataURL(file);
    });

    $('#upload-voucher-form').on('submit', function(event) {
        event.preventDefault();
        $("#upload-animation").toggleClass("hidden");
        $('#send-button').prop('disable', true);
        upload();
    });

    function upload() {
        var formData = new FormData(document.getElementById('upload-voucher-form'));
        formData.append('file', $('#file-input').prop('files')[0]);
        formData.append('url', upload_url);
        formData.append('use_method', 'PUT');

        $("#upload-animation").toggleClass("hidden");
        $('#send-button').prop('disable', false);
        uploadFileAjax(formData, function(response) {
            if (response.status_code === HTTP_CODES.OK) {
                $('#upload-voucher-modal').modal('hide');
                $('#thanks-for-payment-modal').modal('show');
            }
        });
    }
});
