$(document).ready(function () {
    contentTitleQuery = $("#title_query_content"); // Contenedor titulo
    titleQuery = $("#title_query");       // Titulo
    testMessage = $("#text_message"); // Mensaje de texto

    $(document).on('click', testMessage,function(){
        /* Manejar listado de clientes */
        titleQuery.show();
    });
}); // cierra document ready