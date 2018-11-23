
$(function() {
    const HTTP_CODES = {OK:200, CREATED:201, BAD_REQUEST:400, NOT_FOUND:404}

    $(document).ready(function() {
        messageSent = false;
        $('#update-password-button').prop('disabled', true);
    });

    $('#current-password').on('input', checkButton);
    $('#new-password').on('input', validatePassword);
    $('#new-password-retype').on('input', validatePassword);

    function haveInputs() {
        var old_password = $('#current-password').val();
        var new_password = $('#new-password').val();
        var new_password_retype = $('#new-password-retype').val();
        return old_password.length > 0 && new_password.length > 0 && new_password_retype.length  > 0
    }

    function isSamePassword() {
        var new_password = $('#new-password').val();
        var new_password_retype = $('#new-password-retype').val();

        return new_password === new_password_retype;
    }

    function validatePassword(event) {
        if (isSamePassword())
            $('#validation-message').attr('hidden', true);
        else
            $('#validation-message').attr('hidden', false);

        checkButton();
    }

    function checkButton() {
        $('#update-password-button').prop('disabled', !isSamePassword() || !haveInputs() || messageSent);
    }

    $('#update-password-form').on('submit', function(event) {
        event.preventDefault();
        updatePassword();
    });

    function updatePassword() {
        var data = {
            'url': 'change/password/' + user_id + '/',
            'old_password': $('#current-password').val(),
            'password': $('#new-password').val()
        }

        sendAjaxService(data, function(response) {
            console.log("response: ", response)
            messageSent = false;
            checkButton();
            if (response.status_code === HTTP_CODES.OK) {
                $('#update-password-status').html('<span class="successful">Se actualizo satisfactoriamente</span>');
                setTimeout(function() {
                    $("#update-password").modal('hide');
                }, 2000);
            } else if (response.status_code === HTTP_CODES.BAD_REQUEST) {
                $('#update-password-status').html('<span class="error">La contraseña antigua es incorrecta</span>');
            }
        }, 'PUT');

        messageSent = true;
        checkButton();
    }
});
