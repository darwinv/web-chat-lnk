$(document).ready(function () {
    contentTitleQuery = "#title_query_content"; // Contenedor titulo
    textTitleQuery = "#title_query";       // Titulo
    textMessage = "#text_message"; // Mensaje de texto
    closeQuery = "#close_query"; // Mensaje de texto
    
    $(document).on('click', textMessage, function(){
     // Manejar listado de clientes 
        
        $(contentTitleQuery).show();
    });

    $(document).on('click', closeQuery, function(){
     // Manejar listado de clientes 
        
        $(contentTitleQuery).hide();
    });


}); // cierra document ready