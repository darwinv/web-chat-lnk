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
        $("#requery_modal").addClass("hidden");    
    });
    $(document).on('click', ".no-any-requery", function(){
        data = {
            "category_id":category,
            "url": "client/deny_requery/"
        }

        sendAjaxService(data, function (response) {
            $("#requery_modal").addClass("hidden");
        });
    });
}); // cierra document ready
$(document).on('click', ".close-reply", function(){
    $("#reply-content").data("message-reference", null).hide();
    $(".fileinput-remove").click();
});




