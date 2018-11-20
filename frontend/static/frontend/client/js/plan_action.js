
$(function() {
    const ACTION_TRANSFER = "transfer";
    const ACTION_EMPOWER = "empower";
    const ACTION_SHARE = "share";

    const USER_REGISTERED = 0;
    const USER_INVITED = 1;
    const REGISTRATION_SUCCESSFUL = 2;

    const USER_ADDED_MESSAGE = ["User registered", "An invitation will be sent", "Registration successful"];

    const HTTP_CODES = {OK:200, CREATED:201, BAD_REQUEST:400, NOT_FOUND:404}

    const LEGAL_REQUIRED_PHRASE = "Please indicate that you accept the Terms and Conditions";

    $(document).ready(function() {
        $('#available-queries').html(available_queries)

        var email_list_json = window.localStorage.getItem("email_list");
        if (email_list_json) {
            email_list = JSON.parse(email_list_json);
            addUsersFromList(email_list);
            window.localStorage.removeItem("email_list");
        } else {
            email_list = {};
        }

        if (window.localStorage.getItem("email_to_register"))
            window.localStorage.removeItem("email_to_register");

        $('#legal-checkbox')[0].setCustomValidity(LEGAL_REQUIRED_PHRASE);

        $('#check-email-form').find(':submit').prop('disabled', true);
        $('#action-form').find(':submit').prop('disabled', true);
    });

    $('#email-box').keyup(function(){
        $('#check-email-form').find(':submit').prop('disabled', this.value == "" ? true : false);     
    })

    $('#check-email-form').on('submit', function(event) {
        event.preventDefault();
        checkEmail();
    });

    // Funcion que agrega el elemento DOM del usuario y controla los counts
    function addUserToListView(email, type, count) {
        if (action === ACTION_TRANSFER)
                $('#email-box').prop('disabled', true);

        if (count == null)
            count = 0;

        default_message = $("#second-section #default-message").remove();
        var user_line = '';
        user_line += '<div class="row justify-content-center user-line">';
        user_line += '  <div class="col-7 col-sm-6 col-md-5 col-lg-4 email-section">';
        user_line +=      email + '<br />' + USER_ADDED_MESSAGE[type] ;
        user_line += '  </div>';
        if (action === ACTION_SHARE) {
            user_line += '  <div class="col-5 col-sm-4 col-md-3 col-lg-2 count-section">';
            user_line += '    Num of queries<br />';
            user_line += '    <input id="count-for-' + email + '" class="queries-count" type="number" value="' +  count + '"';
            user_line += 'min="1" max="' + available_queries + '">';
            user_line += '  </div>';
        }
        user_line += '</div>';
        $('#second-section').append(user_line);

        if (action === ACTION_SHARE) {
            $('.queries-count').off('input');
            $('.queries-count').on('input', function(event) {
                var email = $(this).attr('id').slice(10);
                count = $(this).val();
                if (count == null || count == '')
                    count = 0;
                else
                    count = parseInt(count, 10);
                email_list[email]['count'] = count;
            });
        }

        $('#action-form').find(':submit').prop('disabled', Object.keys(email_list).length == 0);
    }

    // Funcion para agregar usuarios a la lista de usuarios.
    // Util para chequear si un usuario ya ha sido agregado y para guardar
    // usando localStorage para rellenar la lista despues de regresar
    // @param email: Email del usuario
    // @param type: Tipo de usuario (Registrado anteriormente/Invitado/Registrado ahora)
    // @param count: Contador opcional
    function addUserToList(email, type, count) {
        if (count == null) count = 0;
        email_list[email] = {"type":type, "count":count}
        addUserToListView(email, type, count);
    }

    function addUsersFromList(email_list) {
        for (email in email_list) {
            var type = email_list[email]["type"];
            var count = email_list[email]["count"];
            addUserToListView(email, type, count);
        }
    }

    function checkEmail() {
        var data = {
            "email_receiver": $('#email-box').val(),
            "acquired_plan": acquired_plan,
            "type_operation": type_operation,
            "url": 'clients/email-check-operation/'
        }

        sendAjaxService(data, function(data) {
            var email = $('#email-box').val();
            if (data == null) {
                console.log("data should not be null");
                return;
            }

            if (email in email_list) {
                // TODO: Mostrar el mensaje en un modal
                alert("The email is already in the list")
                return;
            }

            console.log("data: ", data)
            if (data.status_code === HTTP_CODES.OK) {
                addUserToList(email, USER_REGISTERED);
                $('#email-box').val('');
            } else if (data.status_code === HTTP_CODES.NOT_FOUND) {
                $('#new-user-modal').modal('show');
                $('#action-holder').html(email);
            } else if (data.status_code === HTTP_CODES.BAD_REQUEST) {
                if (data.email_receiver) {
                    // TODO Mostrar en modal
                    alert(data.email_receiver)
                } else {
                    console.log("not supported")
                }
            }
        }, "GET");
    };

    $('#send-invitation-btn').on('click', function(event) {
        addUserToList($('#email-box').val(), USER_INVITED);
        $('#email-box').val('');
    });

    $('#register-new-user-btn').on('click', function(event) {
        console.log("register new user btn");
        window.localStorage.setItem("email_list", JSON.stringify(email_list));
        window.localStorage.setItem("email_to_register", $('#email-box').val());
        window.localStorage.setItem("redirect_to", window.location.href);
        window.location.replace(register_url);
    });

    $('#legal-checkbox').click(function() {
        $(this)[0].setCustomValidity($(this)[0].validity.valueMissing ? LEGAL_REQUIRED_PHRASE : '');
    });

    $('#action-form').on('submit', function(event) {
        console.log("calling event")
        event.preventDefault();
        runAction();
    });

    function runAction() {
        var data = {
            "acquired_plan": acquired_plan,
            "url": 'clients/plans-' + action + '/'
        }

        if (action === ACTION_TRANSFER) {
            email_receiver = Object.keys(email_list)[0];
            data['email_receiver'] = email_receiver;
        } else {
            var clients = [];
            var count_sum = 0;
            for (var email in email_list) {
                if (action === ACTION_EMPOWER) {
                    clients.push({"email_receiver":email});
                } else if (action === ACTION_SHARE) {
                    var count = email_list[email]['count'];
                    count_sum += count;
                    clients.push({"email_receiver":email, "count":count});
                }
            }

            if (count_sum > available_queries) {
                alert("Exceeded the limit of available queries");
                return;
            }

            data['client'] = JSON.stringify(clients);
        }
        console.log("input: ", data)

        sendAjaxService(data, function(data) {
            console.log("output: ",  data)
            if (data == null) {
                console.log("data should not be null");
                return;
            }

            if (data.status_code == null) {
                console.log("status code should not be null");
                return;
            }

            if (data.status_code === HTTP_CODES.OK) {
                window.location.replace(final_url);
            } else if (data.status_code === HTTP_CODES.BAD_REQUEST) {
                if (data.detail)
                    alert(data.detail);
            }
        }, "POST");
    }
});
