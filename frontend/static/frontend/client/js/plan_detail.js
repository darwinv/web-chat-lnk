
$(function() {
    const ACTION_TRANSFER = "transfer";
    const ACTION_EMPOWER = "empower";
    const ACTION_SHARE = "share";

    const HTTP_CODES = {OK:"200", CREATED:"201", BAD_REQUEST:"400", NOT_FOUND:"404"}

    $(document).ready(function() {
        $('.drop-down').hide();
    });

    $('.delete-empower-ellipsis').click(function(event) {
        $(this).parent().find('.drop-down').slideToggle(200);
    });

    $(document).click(function(event) { 
        if (!$(event.target).closest('.delete-empower-ellipsis').length) {
            if ($('.delete-empower-ellipsis').parent().find('.drop-down').is(":visible")) {
                $('.delete-empower-ellipsis').parent().find('.drop-down').slideToggle(200);
            }
        }        
    });

    $('.drop-down').click(function(event) {
        var email_receiver = $(this).attr('id').slice(11)

        var data = {
            "email_receiver": email_receiver,
            "acquired_plan": plan_id,
            "url": 'clients/plans-delete-empower/'
        }

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

            if (data.status_code == HTTP_CODES.OK || data.status_code == HTTP_CODES.NOT_FOUND) {
                var selector = '#' + email_receiver.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
                $(selector).next().remove();
                $(selector).remove();
            } else if (data.status_code == HTTP_CODES.BAD_REQUEST) {
                if (data.detail)
                    alert(data.detail);
            }
        }, "POST");
    });
});
