
$(function() {
    const HTTP_CODES = {OK:"200", CREATED:"201", BAD_REQUEST:"400", NOT_FOUND:"404"}

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
        upload();
    });

    function upload() {
        var url = "http://192.168.1.3:8080/" + upload_url;
        var data = {
            'url': upload_url
        }

        var formData = new FormData(document.getElementById('upload-voucher-form'));
        //formData.append('file', $('#file-input').prop('files')[0]);
        formData.append('data', JSON.stringify(data));

        console.log("----ENTRIES----")
        for (var p of formData)
            console.log("entry: ", p)
        console.log("--ENDOFENTRIES--")

        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajax({
            type: "POST",
            beforeSend: function(request, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    request.setRequestHeader("X-CSRFToken", csrftoken);
                }
                // Recorre cabeceras por clave y valor
                for (var key in headers){
                    if (headers.hasOwnProperty(key)) {
                        request.setRequestHeader(key, headers[key]);
                    }
                }
            },
            url: AJAX_SERVICE,
            data: formData,
            //dataType: "json",
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("response: ", response)
            }
        });
    }
});
