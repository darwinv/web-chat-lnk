$(document).ready(function () {
    /*Variables generales del archivo*/
    var dataRoom = getDataRoom()
    var category = dataRoom["category"];


    
    contentTitleQuery = "#title_query_content"; // Contenedor titulo
    textTitleQuery = "#title_query"; // Titulo
    textMessage = "#text_message"; // Mensaje de texto
    closeQuery = "#close_query"; // Mensaje de texto
    
    $(document).on('click', textMessage, function(){
        // Manejar listado de clientes
        var messageReference = $("#reply-content").data("message-reference");
        if (!messageReference) {
            // Si no estoy haciendo reconsulta..
            // Muestro titulo
            $(contentTitleQuery).show().find("input").prop("disabled", false );
        }
    });

    $(document).on('click', closeQuery, function(){
        // Manejar listado de clientes
        $(contentTitleQuery).hide().find("input").prop("disabled", true);
    });

    $(document).on('click', ".close-requery-modal", function(){
        visibleForRequery(false);   
    });
    $(document).on('click', ".no-any-requery", function(){
        data = {
            "category_id":category,
            "url": "client/deny_requery/"
        }

        $("#animacion").toggleClass("hidden");
        $("#requery_modal").find("button").attr("disabled", true);
        sendAjaxService(data, function (response) {
            $("#animacion").toggleClass("hidden");
            $("#requery_modal").find("button").attr("disabled", false);
            visibleForRequery(false);
        });
    });

    $(document).on('click', "#send_punctuation", function(){
        var qualification = $("#punctuation_modal img.selected").data("qualification");
        var query = $("#punctuation_modal").data("query");
        data = {
            "url": `client/qualify/queries/${query}/`,
            "qualification": qualification
        }
        $("#animacion").toggleClass("hidden");
        $("#punctuation_modal").find("button").attr("disabled", true);
        sendAjaxService(data, function(response){
            $("#animacion").toggleClass("hidden");
            $("#punctuation_modal").find("button").attr("disabled", false);

            if (response.status_code==200) {
                queriesToCalificate.shift();
                if (queriesToCalificate.length > 0 && roleID == ROLES.client) {
                    $("#punctuation_modal").data("query",queriesToCalificate[0]);
                }else{
                    visibleForPunctuation(false);
                }

            }else{
                // Error
                console.log(response);
            }            
        },"PUT")
    });

}); // cierra document ready
$(document).on('click', ".close-reply", function(){
    $("#reply-content").data("message-reference", null).hide();
    $(".fileinput-remove").click();
});

$(document).on('click', "#punctuation_modal img", function(){
    $("#punctuation_modal img").removeClass("selected");
    $(this).addClass("selected");
});

function visibleForPunctuation(show){
    if (show) {
        $("#upload-div, #errors_alert, #animacion, #requery_modal, #form-chat").addClass("hidden");
        $("#punctuation_modal").removeClass("hidden");
    }else{
        $("#punctuation_modal").addClass("hidden");
        $("#form-chat").removeClass("hidden");
    }             
}
function visibleForRequery(show){
    if (show) {
        $("#upload-div, #errors_alert, #animacion, #punctuation_modal, #form-chat").addClass("hidden");
        $("#requery_modal").removeClass("hidden");
    }else{
        $("#requery_modal").addClass("hidden");
        $("#form-chat").removeClass("hidden");
    }
}



