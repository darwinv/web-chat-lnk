$(document).ready(function () {

    $('#view_match_modal').on('shown.bs.modal', function (e) {
        // Cuando abre vista modal
        var matchId = $(e.relatedTarget).data('id');
        $(e.currentTarget).find('#open_decline_modal').data('matchid', matchId);
        $(e.currentTarget).find('#open_accept_modal').data('matchid', matchId);
        // console.log($('#open_decline_modal').data('matchid')+"hey");
        // var categoryImg = `<center> <img src="{{ match.category_image }}" alt="imagen-especialidad"> </center>`;
        var categoryImg = $("#match_"+matchId).find('img').clone();
        var subject = $("#match_"+matchId).find('p.subject_match').text()
        var attachments = $("#match_"+matchId).find('.files').html()
        categoryImg.appendTo($(e.currentTarget).find('.speciality-img'));
        $(e.currentTarget).find('.subject').html('<h4> Asunto </h4>'+ subject);
        $(e.currentTarget).find('.files_match').html(attachments);


      });


    $('#view_match_modal').on('hidden.bs.modal', function () {
        $(".container-modal-match .subject").empty();
        $(".container-modal-match .speciality-img").empty();
        $(".container-modal-match .files_match").empty();
        // $("#message").empty();
        // $("#message").removeClass();
            // do something…
    });

    $('#decline_match_modal').on('shown.bs.modal', function (e) {
        $('#view_match_modal').modal('hide');
        var matchId = $(e.relatedTarget).data('matchid');
        $(e.currentTarget).find('#decline').data('matchid', matchId);
    }); 

    $('#accept_match_modal').on('shown.bs.modal', function (e) {
        $('#view_match_modal').modal('hide');
        var matchId = $(e.relatedTarget).data('matchid');
        $(e.currentTarget).find('#accept').data('matchid', matchId);
        console.log(matchId);
    }); 

    $('#decline_match_modal').on('hidden.bs.modal', function () {
        $("#decline_motive").val('');
    });
   

        // Declinar Match Specialista
    $(document).on('submit','#decline-match',function(event){
            event.preventDefault();
            $("#decline_match_modal #animacion1").toggleClass("hidden");
            var win = $("#decline-match").find('#decline');
            var declinedMotive = $("#decline-match").find('#decline_motive').val();
            data = {
                "url": `specialists/decline/matchs/${win.data("matchid")}`,
                "declined_motive": declinedMotive
                }
            
                $("#decline").attr("disabled", true);
                sendAjaxService(data, function(response) {
                if (response.status_code == "200") {
                    $('#decline_match_modal #message').addClass('successful');
                    $('#decline_match_modal #message').text("Match se ha Declinado");
                    $("#decline_match_modal #animacion1").toggleClass("hidden");
                    setTimeout(function(){
                        $("#decline_match_modal").modal('hide');
                        $("#decline_match_modal .close").click();
                      }, 2000);                    
                    location.reload();
                } else{
                    $("#animacion1").toggleClass("hidden");
                    $("#decline").removeAttr("disabled");
                    if(response.status_code == "400") {
                        if(response.declined_motive) {
                            $('#message').text("error: Motivo de declinacion"+ response.declined_motive );  
                        }
                    }
                }      

                }, type="PUT")

        });

        $(document).on('click','#accept',function(event){
            event.preventDefault();
            $("#accept_match_modal #animacion1").toggleClass("hidden");
            var win = $("#accept-match").find('#accept');
            
            if($('#discount').is(':checked')){
                option_payment = 2;   
            }
            data = {
                "url": `specialists/accept/matchs/${win.data("matchid")}`,
                "payment_option_specialist": option_payment
                }
            if (option_payment == 2) {
                $("#match").attr("disabled", true);
                sendAjaxService(data, function(response) {
                    if (response.status_code == "200") {
                        $('#accept_match_modal #message').addClass('successful');
                        $('#accept_match_modal #message').text("Match se ha aceptado");
                        $("#accept_match_modal #animacion1").toggleClass("hidden");
                        setTimeout(function(){
                            $("#accept_match_modal").modal('hide');
                            $("#accept_match_modal .close").click();
                          }, 2000);                    
                        location.reload();
                    } else{
                        $("#accept_match_modal #animacion1").toggleClass("hidden");
                        $("#accept").removeAttr("disabled");
                        if(response.status_code == "400") {
                            if(response.payment_option_specialist) {
                                $('#accept_match_modal #message').text("error: Opcion de pago"+ response.payment_option_specialist);  
                            }
                        }
                    }      
    
                    }, type="PUT")   

            }
        });     

});