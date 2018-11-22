
$(function() {
    const HTTP_CODES = {OK:200, CREATED:201, BAD_REQUEST:400, NOT_FOUND:404}

    $(document).ready(function() {
        console.log("LOADED")
    });

    $('#activation-button').click(function(event) {
        console.log("about to show the modal")
        $('#activation-modal').modal('show');
    });

    $('#pin-box').on('input', function(event) {
         var pin = $(this).val()
         if (pin.length >= 4) {
            activation(pin, 'GET', function(response) {
                if (!response) {
                    console.log("response shouldn't be null");
                }

                if (!response.status_code) {
                    console.log("response should have an status code");
                }

                console.log("response: ", response)

                if (response.status_code === HTTP_CODES.OK) {
                    console.log("status code is 200 (ok)")
                    var details = '';
                    details += '<div id="detail" class="col-12">';
                    details += '    <span id="detail-title">DETAIL OF THE PLANS</span><br />';
                    details += '    Nombre de plan: ' + response.plan_name + '<br />';
                    details += '    Cantidad de consultas: ' + response.query_quantity + '<br />';
                    details += '    Consultas disponibles: ' + response.available_queries + '<br />';
                    details += '    Validez: ' + response.validity_months + ' meses<br />';
                    details += '    Precio: ' + response.price + '<br />';
                    details += '    Esta activo: ' + (response.is_active ? "Yes" : "No") + '<br />';
                    details += '</div>'
                    $('#detail-section').append(details);
                } else if (response.status_code === HTTP_CODES.NOT_FOUND) {
                    $('#detail').remove();
                }
            });
        }
    });

    $('#activation-form').on('submit', function(event) {
        event.preventDefault();
        var pin = $('#pin-box').val();
        console.log("pin: ", pin)
        $("#activation-animation").toggleClass("hidden");
        $('#activate-button').prop('disable', true);
        activation(pin, 'PUT', function(response) {
            $("#activation-animation").toggleClass("hidden");
            $('#activate-button').prop('disable', false);
            if (!response) {
                console.log("response shouldn't be null");
            }

            if (!response.status_code) {
                console.log("response should have an status code");
            }

            console.log("response: ", response)

            if (response.status_code === HTTP_CODES.OK) {
                $('#response-message').html('<span class="successful">Activacion satisfactoria</span>');
                var plan_id = response.id
                setTimeout(function() {
                    $(document).trigger("activation", [plan_id]);
                    $("#activation-modal").modal('hide');
                }, 2000);
            } else if (response.status_code === HTTP_CODES.NOT_FOUND) {
                $('#response-message').html('<span class="error">No se encuentra ese plan</span>');
            }
        })
    });

    function activation(pin, method, callback) {
        var data = {'url':'activations/plans/' + pin + '/'}
        sendAjaxService(data, callback, method);
    }
});
