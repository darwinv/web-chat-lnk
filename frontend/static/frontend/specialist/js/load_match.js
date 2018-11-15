$(document).ready(function () {

    $('#view_match_modal').on('shown.bs.modal', function (e) {
        // Cuando abre vista modal de los planes
        var win = $('#change-chosen-list'); // Contenedor listado   
        //Inicializando data 
        win.data("url",'clients/plans/');  // Url a consumir
        win.data("page", 0);  // Inicializacion de pagina en 0, solo Modales
        win.data("lastScrollTop", -1) // Inicializamos variable Top solo Modales
        loadPlansChange(win);
      });

)};