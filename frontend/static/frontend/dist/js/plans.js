

$(function() {
    var email_list = []

    $('#check-email-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        checkEmail();
    });

    function checkEmail() {
        console.log('check_email is working')
        data = {
            "email_receiver": $('#email-box').val(),
            "acquired_plan": acquired_plan,
            "type_operation": type_operation,
            "url": 'clients/email-check-operation/'
        }

        sendAjaxService(data, function(data) {
            console.log("from ajax response");
            email = $('#email-box').val();
            $('#email-box').val('');

            if (!data) {
                console.log("data should not be null");
                return;
            }

            if (data == true) 
                onUserRegistered(data);
            else if (data.detail)
                onUserNotRegistered(data);
        }, "GET");
    };

    function addUSerToList(email, message) {
        if (email_list.includes(email)) {
            // TODO: Mostrar el mensaje en un modal
            alert("The email is already in the list")
            return;
        }

        email_list.push(email);
        if (action == "transfer")
                $('#email-box').prop('disabled', true);
        $("#second-section #default-message").remove();
        $('#second-section div ul').append('<li class="user-line">' + email + '<br />' + message + '</li>');
    }

    function onUserRegistered(data) {
        console.log("user registered");
        addUSerToList(email, "User registered")
    }

    function onUserNotRegistered(data) {
        console.log(data.detail);
        $('#new-user-modal').modal('show');
        $('#action-holder').html(email)
    }

    $('#send-invitation-btn').on('click', function(event){
        console.log("send invitation btn")
        addUSerToList(email, "An invitation will be sent")
    });

    $('#register-new-user-btn').on('click', function(event){
        console.log("register new user btn")
    });
});
