$(document).ready(function () {
  (function( $ ){
   $.fn.getScrollHeight = function() {
    // Funcion que retorna la altura de un elemento
    var win = document.getElementById(this.attr('id'));
    return win.scrollHeight - win.clientHeight;
  }; 
  })( jQuery );

  (function( $ ){
   $.fn.canMakeScrollPagination = function() {
    // Funcion para calcular realizacion de paginacion
    var win = document.getElementById(this.attr('id'));
    var positionScroll = win.scrollTop;
    var diffScroll = win.scrollHeight - win.clientHeight;
    var resScroll = positionScroll / diffScroll;
    
    if (resScroll >= 0.9){
      return true
    }else{
      return false
    }
   }; 
  })( jQuery );

  (function( $ ){
    // DATA ATRIBUTES
    // win.data("url",'clients/plans/');  Requerido: Url a consumir
    // win.data("page", 0);  Opcional: Inicializacion de pagina en 0 (Modals)
    // win.data("lastScrollTop", -1) Opcional: Inicializamos variable Top (Modals)
   $.fn.sendAjaxPagination = function(clouserPagination) {
    // FUNCION GENERICA PARA REALIZAR GET AJAX PARA PAGINACION
    // clouserPagination funcion a ejecutar call back
    // parameters: objeto con valores filtrables
    
    // Variables externas que necesitan ser definidas    
    //AJAX_SERVICE: url genica para servicios get en el servidor
    //LOADING_HTML: html funcional de un cargando
        
    $window = this;
    var st = $window.scrollTop();
    var idElement = $window.attr('id');

    if (AJAX_SERVICE === undefined) {
      return;
    }
    if ($window.data('requestRunning') === false) {
      // Procesando request or Scroll Up
      return;
    }    
    if ($window.data('lastScrollTop') === undefined) {
      $window.data('lastScrollTop', -1); // Inicializacion del Scroll Up
    }
    if (st <= $window.data('lastScrollTop')) {
      // Procesando request or Scroll Up
      $window.data('lastScrollTop', st);
      return;
    }
    if (LOADING_HTML === undefined) {
      LOADING_HTML = "";
    }

    $window.data('requestRunning', false);
    $window.data('lastScrollTop', st);
    $window.append(LOADING_HTML);
    // Create loading on footer list Win.loading
    page = $window.data("page");
    url = $window.data("url");
    
    if (page === undefined){
      page = 1;
    }else{
      page++;
    }
    var data = {'page':page, 'url':url, 'parameters':parameters}

    // $window.animate({ scrollTop: $window.getScrollHeight() }, 100);

    $.ajax({
        url: AJAX_SERVICE,
        dataType: 'json',
        data: data,
        success: function(data) {
          clouserPagination(data);
          if (data.results) {
            $window.data("page", page);
          }
        },
        complete: function() {
            $window.data('requestRunning', true);
            $window.find(".loading-html").remove();
        }
    });
    return this;
   }; 
  })( jQuery );
});