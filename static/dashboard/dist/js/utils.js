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
    parameters = $window.data("parameters");

    if (page === undefined){
      page = 1;
    }else{
      page++;
    }
    var data = {'page':page, 'url':url};
    
    if (typeof(parameters) == "object"){
      data = Object.assign({}, data, parameters);
    }
    $.ajax({
        url: AJAX_SERVICE,
        dataType: 'json',
        data: data,
        success: function(data) {
          clouserPagination(data);

          if (data && data.results) {
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



  String.prototype.format_hard = function () {
    args = arguments;    
    a = this
    for (var key in args[0]) {
      // skip loop if the property is from prototype
      if (!args[0].hasOwnProperty(key)) continue; 
      a = a.replace("{"+key+"}", function () {
        response = typeof args[0][key] != 'undefined' ? args[0][key] : '';
        return response
      });

    }
    return a
    
  };

  String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {      
      response = typeof args[i] != 'undefined' ? args[i] : '';
      i++
      return response
    });
  };

});
/*AJAX Service*/
function sendAjaxService(data, clouserSuccess, type='POST'){
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

  $.ajax({
    type: type,
    beforeSend: function(request, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            request.setRequestHeader("X-CSRFToken", csrftoken);
        }
        // Recorre cabeceras por clave y valor
      for (var key in headers){
        if (headers.hasOwnProperty(key)) {
          request.setRequestHeader(key, headers[key]);
        }
      }
    },
    url:AJAX_SERVICE,
    data:data,
    dataType: "json",
    success: function(response) {
      clouserSuccess(response);
    }
  });
}

function uploadFileAjax(formData, successCB) {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "POST",
        beforeSend: function(request, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            }
            // Recorre cabeceras por clave y valor
            for (var key in headers){
                if (headers.hasOwnProperty(key)) {
                    request.setRequestHeader(key, headers[key]);
                }
            }
        },
        url: AJAX_SERVICE,
        data: formData,
        //dataType: "json",
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(response) {
            successCB(response);
        }
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function renderTypeMessage(message) {
  console.log(message);
    // Retorna contenido del mensaje segun tipo de mensaje
    response = '';
    if (message.file_url) {
      message.fileUrl = message.file_url;
      message.filePreviewUrl = message.file_preview_url;
      message.fileType = message.content_type;
    }
    

    if (message.fileType == 1){
        response  = `<div class="chat-text-thumb">
                <p class="text">${message.message}</p>
            </div>`;
    } else if (message.fileType == 2){
        response  =    `<div class="chat-img-thumb chat_play_medias"
            data-file-url="${message.fileUrl}">
                <img src="${message.filePreviewUrl}">
            </div>`;
    }else if(message.fileType == 3){
        response  =`<div class="chat-video-thumb chat_play_medias" data-file-url="${message.fileUrl}">
            <img src="${message.filePreviewUrl}">
            <div class="play-video">
                <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><g id="Page-1" fill="none" fill-rule="evenodd"><g id="media-play" transform="translate(4 2.5)" fill="#FFF"><path d="M15.5 7.9L2.5.4C1.2-.3.1.3.1 1.8v15c0 1.5 1.1 2.1 2.4 1.4l13-7.5c1.3-.9 1.3-2.1 0-2.8z" id="Path"></path></g></g></svg>
            </div>
        </div>`;
    }else if(message.fileType == 4){
        response  =`<div class="chat-audio-thumb text-center">
           <audio controls>
              <source src="${message.fileUrl}" type="audio/ogg">
              <source src="${message.fileUrl}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>`;
    }else if(message.fileType == 5){
        if (message.uploaded == 2){
            atag = `<a target="_blank" href="${message.fileUrl}">Descargar Archivo</a>`
        }
        else{
            atag = `<a href="#">Archivo no encontrado</a>`
        }

        response  =`<div class="chat-file-thumb text-center">
                        <i class="fas fa-file"></i>
                        ${atag}
                    </div>`;
    }
    return response;
}

$(document).on('click', ".chat_play_medias", function(){
    
    msg = $(this).parents(".message");
    console.log($(this));
    if (msg.data("uploaded")==1 || msg.data("uploaded")==5) {
        return false;
    }

    var url = $(this).data("file-url");
    if ($(this).hasClass("chat-video-thumb")) {
        // Show videos
        $("#modal_play_medias").find(".modal-body video").show(
            ).attr('src', url);
        $("#modal_play_medias").find(".modal-body img").hide();
    }else if ($(this).hasClass("chat-img-thumb")){
        // Show imgs
        $("#modal_play_medias").find(".modal-body video").hide();
        $("#modal_play_medias").find(".modal-body img").show().attr(
        'src', url);
    }

    $('#manage_query_specialist').modal('hide');
    $('#modal_play_medias').modal('show');
});