$(document).ready(function () {
    $(".match").each(function(){
        // Renderizamos el time en el listado
        // le damos  formato a de fecha a todas las fechas de match
        var timeMatch = $(this).data("time");
        var status = $(this).data("status");
        var timeMatchFixed = dateTextCustom(moment.utc(timeMatch), "-05:00");
        $(this).find("small.time").text('Solicitado: '+ timeMatchFixed);
        if (status == 1){
            $(this).find("p.status").text("Estado: Esperando Respuesta");
        }
    });

    var win = $("#list-match-content");
    win.data("url",'client/matchs/');  // Url a consumir
    win.data("page", 1);  // Inicializacion de pagina en 0, solo Modales
    win.sendAjaxPagination(function(resp){
        console.log(resp);
    });
});