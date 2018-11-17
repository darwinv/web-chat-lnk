$(document).ready(function () {
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
        $(contentTitleQuery).show().find("input").prop("disabled", true);
    });


}); // cierra document ready
$(document).on('click', ".close-reply", function(){
    $("#reply-content").data("message-reference", null).hide();
    $(".fileinput-remove").click();    
});