
var queriesToCalificate = []
$(function() {

updateMessage(); //se llama a la funcion change message
if ($('#chat_box .globe-chat').length) {
  scrollDown(); // si existe al menos uno  Scrolleamos hasta abajo
}
/*Variables generales del archivo*/
var dataRoom = getDataRoom()
var userRoom = dataRoom["userRoom"];
var category = dataRoom["category"];
var chatsock = connectingWebSocket();


chatsock.onopen = function open() {
    console.log('WebSockets connection created.');
};
chatsock.onmessage = function(message) {
    var data = JSON.parse(message.data);

    if (data.eventType == 1) {
        renderMessages(data);
    }else if (data.eventType == 2) {
        updateQuery(data);
    }else if (data.eventType == 3) {
        updateFiles(data);
    }else{
        console.log('Evento Desconocido Sockets');        
        console.log(data);
    }
};
function updateQuery(data){ 
    query = data.query
    for (var key in data.data) {
        // skip loop if the property is from prototype
        if (!data.data.hasOwnProperty(key)) continue;
        var obj = data.data[key];
        $(".query_"+query).data(key, obj).addClass(".no-ready-message");
    }
    
    updateMessage();
}
function updateFiles(data){
    query = data.query
    $.each(data.messages, function(key,value){
        $("#message_"+value.id).prop("src", value.filePreviewUrl);
        $("#message_"+value.id).data("file-url", value.fileUrl);
    });
}

function renderMessages(data){
    var audio = new Audio(audioNotification);
    var boxChat = $("#chat_box");
    var chat_box = document.getElementById("chat_box");
    var positionScroll = chat_box.scrollTop;
    var diffScroll = chat_box.scrollHeight - chat_box.clientHeight;
    var resScroll = positionScroll / diffScroll;
    var specialistMsg = data.specialist;
    var showRequery = false;

    if (roleID==ROLES.client) {
        var actionsEvents = `<a class="dropdown-item query-event-reply" href="#">Reconsulta</a>`;            
    }else{
        var actionsEvents = `<a class="dropdown-item query-event-reply" href="#">Responder</a>
                             <a class="dropdown-item query-event-derive"
                                href="#">Derivar</a>`; 
    }
    var actions = `<div class="dropdown chat-angle-down" >
                  <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  </button>
                  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    ${actionsEvents}
                  </div>
                </div>`;

    $.each(data.messages, function(key,value){
        var msg = value.message;
        var codeUser = value.codeUser;        
        var msgType = value.messageType;
        var groupStatus = value.groupStatus;

        
        if (specialistMsg == userID && groupStatus == 1 && (msgType =="q" || msgType =="r") ){
            actions_temp = actions;
        }else if(groupStatus == 1 && msgType == "a" && roleID == ROLES.client){
            actions_temp = actions;
            showRequery = true;
        }else{
            actions_temp = "";
        }

        var divMessage = `<div class='row globe-chat'>
                                <div class='cont-title-query' 
                                style='display: none'>
                                    <div class='title-query'>
                                        ${data.query}
                                    </div>
                                </div>
                                <div id='message_${value.id}' class='message col-sm-6 
                                col-sm-offset-6 query_${value.query_id} no-ready-message'
                                data-sender='${value.user_id}' 
                                data-timemessage='${value.timeMessage}' 
                                data-query='${value.query_id}'
                                data-message='${value.id}'
                                data-msg-type='${msgType}'
                                data-msg-specialist='${specialistMsg}'
                                >
                                    ${actions_temp}
                                    <div class='row'>
                                        <div class='col-sm-12'>
                                            ${renderTypeMessage(value)}
                                        </div>
                                    </div>
                                    <div class='row marT10 message-footer'>
                                        <div class='col-sm-6'>
                                            <p class='code-user'>
                                                ${value.codeUser}
                                            </p>
                                        </div>
                                        <div class='col-sm-6'>
                                            <p>
                                                <small class='time'></small>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>`;

        boxChat.append(divMessage);        
    });
    
    updateMessage();
    // Calculo la diferencia de pixeles entre el ultimo msj y el scroll
    if (resScroll >= 0.9){
        scrollDown();
    }

    if (showRequery) {
        $("#requery_modal").removeClass("hidden");
        $("#reply-content").data("message-reference", null).hide();
        $(".fileinput-remove").click();
    }
}





if (chatsock.readyState == WebSocket.OPEN) {
    chatsock.onopen();
}

$("#form-chat").submit(function(e){
    e.preventDefault();
    var textMessage = $('#text_message').val(); 
    var messageReference = $("#reply-content").data("message-reference");

    if (messageReference) {
        query = $("#reply-content").data("query-reference");
        // Respuestas o Reconsultas
        if (roleID==ROLES.specialist) {
            var messageType = 'a';
        }else{
            var messageType = 'r';
        }
        var dataQuery = {
            query: query,
            message: [{
                msg_type: messageType,
                message: textMessage,
                content_type: 1,
                file_url: '',
                message_reference: messageReference
            }],
        };
    }else{
        // Nuevos Queries
        var title = $('#title').val();  
        var messageType = 'q';
        var dataQuery = {
            title: title,
            category: category,
            message: [{
                msg_type: messageType,
                message: textMessage,
                content_type: 1,
                file_url: ''
            }],
        };
    }
    
    ajaxQuery(dataQuery);
});

function ajaxQuery(dataQuery, messageReference){
    var arrFiles = getMessageFiles(dataQuery["message"][0]["msg_type"]);
    dataQuery["message"] = dataQuery["message"].concat(arrFiles);

    $("#animacion").toggleClass("hidden");
    var csrfToken = $('[name=csrfmiddlewaretoken]').val(); 
    // Funcion para enviar ajax a query
    $(".send-message-cont").find("button").attr("disabled", true);
    $("#errors_alert").addClass("hidden").find("li").remove();
    $.ajax({
        beforeSend: function(request, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              request.setRequestHeader("X-CSRFToken", csrfToken);
            }
            // Recorre cabeceras por clave y valor
            for (var key in headers){
              if (headers.hasOwnProperty(key)) {
                request.setRequestHeader(key, headers[key]);
              }
            }
        },
        type: "POST",
        url: URL_SEND_QUERY,
        data: {
            query_data:JSON.stringify(dataQuery)
        },
        success: function(response){
            if (!$("#animacion").hasClass('hidden')){
                $("#animacion").addClass("hidden");
            }
            $(".send-message-cont").find("button").attr("disabled", false);

            if (response.status_code == 200 || response.status_code == 201) {
                // Query exitoso
                $("#title").val('');
                $("#text_message").val('').focus();
                $("#reply-content").data("message-reference", null).hide();

                
                if (dataQuery["query"]) {
                    $(".query_"+dataQuery["query"]).find(".chat-angle-down").css('display','none');
                }

                if (arrFiles.length > 0) {
                    sendFilesMessages(response);
                }
                
            }else{
                console.log(response);
                if (typeof(response.non_field_errors)=="object") {
                    for (var key in response.non_field_errors) {
                        // skip loop if the property is from prototype
                        if (!response.non_field_errors.hasOwnProperty(key)) continue;
                        var obj = response.non_field_errors[key];
                        $("#errors_alert").append(`<li>${obj}</li>`);
                    }
                }else if (typeof(response.non_field_errors)=="string") {
                    $("#errors_alert").append(`<li>${response.non_field_errors}</li>`);
                }else if (typeof(response)=="object") {
                    for (var key in response) {
                        // skip loop if the property is from prototype
                        if (!response.hasOwnProperty(key)) continue;
                        if (key=="status_code") continue;
                        
                        var obj = response[key];
                        $("#errors_alert").append(`<li>${key}: ${obj}</li>`);
                    }
                }

                $("#errors_alert").removeClass("hidden");
            }
        }
   });

}


$(document).on('click', ".query-event-reply", function(){
    var globeChat = $(this).parents(".globe-chat");
    var reference = globeChat.find(".message").first();
    var messageReference = reference.data("message");
    var queryReference = reference.data("query");
    var titleQuery = globeChat.data("title-query");
    var textMessage = globeChat.find(".chat-text-thumb").first().html();

    if (!textMessage) {
        textMessage = "<i class='fas fa-file'></i> Archivo Adjunto";
    }
    $("#reply-content").find(".message-reference-title").html(titleQuery);

    $("#reply-content").find(".message-reference-message").html(textMessage);
    $("#reply-content").data("message-reference", messageReference);
    $("#reply-content").data("query-reference", queryReference).show();
    $("#title_query_content").hide().find("input").prop("disabled", true );

    if (roleID==ROLES.specialist) {
        $("#selection_message_alert").hide();
        $(".send-message-cont").show();
    }
});



$(document).on('click', ".chat_play_medias", function(){
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

    $('#modal_play_medias').modal('show');
});
$(document).on('click', '#close_errors_alert', function(){
    // Manejar listado de clientes
    $("#errors_alert").addClass("hidden").find("li").remove();
});
function getMessageFiles(messageType){
    /*Traer los archivos como mensajes*/
    var arrFiles = []
    var files = $('#file-linkup').fileinput('getFileStack');

    for (i = 0; i < files.length; i++) {
        typeSplit = files[i].type.split("/");
        var contentType = 5;
        if (typeSplit[0] == 'image'){
            contentType = 2;
        }
        else if (typeSplit[0] == 'video'){
            contentType = 3;
        }
        else if (typeSplit[0] == 'audio'){
            contentType = 4;
        }

        arrFiles[i] = {
            msg_type: messageType,
            message: '',
            content_type: contentType,
            file_url: files[i].name
        }
    }
    return arrFiles;
}

function sendFilesMessages(response){
    var arrFiles = []
    var files = $('#file-linkup').fileinput('getFileStack');

    var filesId = response["message_files_id"]
    var date = new Date();
    var datestring = date.yyyymmdd();    


    var data = new FormData();
    data.append('query', response.query_id);
    $.each(files, function(i, file) {

        typeSplit = file.type.split("/");
        prefixFile = "DOC";

        if (typeSplit[0] == 'image'){
            prefixFile = "IMG";
        }
        else if (typeSplit[0] == 'video'){
            prefixFile = "VID";
        }
        else if (typeSplit[0] == 'audio'){
            prefixFile = "AUD";
        }

        extension = (/[.]/.exec(file.name)) ? /[^.]+$/.exec(file.name) : undefined;
        fileName = `${prefixFile}-${datestring}-${filesId[i]}.${extension}`;
        //Agregando file al formulario
        data.append("file-"+i, file, fileName);
    });


    csrfToken = $('[name=csrfmiddlewaretoken]').val();
    
    $('#upload-div').addClass('hidden');
    $.ajax({
        beforeSend: function(request, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              request.setRequestHeader("X-CSRFToken", csrfToken);
            }
            // Recorre cabeceras por clave y valor
            for (var key in headers){
              if (headers.hasOwnProperty(key)) {
                request.setRequestHeader(key, headers[key]);
              }
            }   
        },
        method: "POST",
        enctype: 'multipart/form-data',
        url: URL_UPLOAD_FILE_QUERY,
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response){
            $('#file-linkup').fileinput('clear');
        }
   });

}

function connectingWebSocket(){
    /*Gestion de conneciones*/
    var ws_scheme = window.location.protocol == "http:" ? "wss" : "ws";
    //conformamos la url para conectar via ws
    api_url = apiUrl.replace("http","ws");
    // Nuestra sala, sera `id_usuario-id_categoria`
    var room = userRoom + '-' + category;
    return new ReconnectingWebSocket(`${api_url}/chat/${room}`);
}



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function scrollDown(){
    var ultimo = $("#chat_box .globe-chat:last").position().top;
    var scrollchat = $("#chat_box").scrollTop();
    $("#chat_box").animate({scrollTop:ultimo+scrollchat});
}

Date.prototype.yyyymmdd = function() {
  var mm = this.getMonth() + 1; // getMonth() is zero-based
  var dd = this.getDate();

  return [this.getFullYear(),
          (mm>9 ? '' : '0') + mm,
          (dd>9 ? '' : '0') + dd
         ].join('');
};




function updateMessage(){
    // Mostrar un solo titulo por grupo de query

    var previus_query_id = $(".message.no-ready-message:first").parents('.globe-chat').prev(".globe-chat").find(".message").data("query");
    
    $(".message.no-ready-message").each(function(){
        var msg = $(this);
        // Renderizamos el time en el listado
        var timeMessage = msg.data("timemessage");
        var msgType = msg.data("msg-type");
        var specialistMsg = msg.data("specialist");
        var groupStatus = msg.data("group-status");
        var queryStatus = msg.data("status");
        var query = msg.data("query");

        timeMessage = toLocalTime(timeMessage);
        msg.find("small.time").text(timeMessage)        

        if (roleID == ROLES.client){
            if(msgType == "a"){
                msg.removeClass("col-sm-offset-6");
                msg.addClass("message-left");
            }else{           
                msg.addClass("message-right");            
            }
        }else if (roleID == ROLES.specialist){
            if(msgType == "a"){
                msg.addClass("message-right");
            }else{
                msg.removeClass("col-sm-offset-6");
                msg.addClass("message-left");
            }
        }

        // Aciones sobre mensaje
        if (specialistMsg == userID && groupStatus == 1 && (msgType =="q" || msgType =="r") ){            
            msg.find(".dropdown-menu").append(`<a class="dropdown-item query-event-derive"
             href="#">Derivar</a>`);
            msg.find(".query-event-reply").html(`Responder`);            
            msg.find(".chat-angle-down").css('display','');
        }else if(groupStatus == 1 && msgType == "a" && roleID == ROLES.client){
            msg.find(".chat-angle-down").css('display','');
        }else{
            msg.find(".chat-angle-down").css('display','none');            
        }

        if (query != previus_query_id){
            msg.siblings(".cont-title-query").show();
            previus_query_id = query;
        }else{
            msg.siblings(".cont-title-query").remove();
        }
        msg.removeClass("no-ready-message");
    
        
        if (queryStatus==4 && !queriesToCalificate.includes(query)) {

            queriesToCalificate.push(msg.data("query"));
        }
    });

    if (queriesToCalificate.length > 0 && roleID == ROLES.client) {
        $("#punctuation_modal").data("query",queriesToCalificate[0]).removeClass("hidden");
    }
}


});
function renderTypeMessage(message) {
    // Retorna contenido del mensaje segun tipo de mensaje
    response = '';
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
        response  =`<div class="chat-file-thumb text-center">
            <i class="fas fa-file"></i>
            <a href="${message.fileUrl}">Descargar Archivo</a>
        </div>`;
    }

    return response;
}

// Funcion para devolver la fecha actual del mensaje
// segun la zona horaria
function toLocalTime(date){
    var dateMsj = new Date(date);
    var hoy = new Date();
    // var ayer = new Date(hoy.getTime() - 24*60*60*1000);
    if (hoy.getDate() === dateMsj.getDate()){
      return String(dateMsj.getHours()) + ':' + String(dateMsj.getMinutes());
    }
    else if (dateMsj.getDate() === hoy.getDate() - 1) {
      return "Ayer";
    }
    else {
      return dateMsj.toLocaleDateString();
    }
}
function getDataRoom(){
    var cadena = window.location.pathname.split("/");
    if (roleID == ROLES.client){
        //extraemos el id actual de usuario
        var userRoom = userID
        //extraemos la categoria
        var category = cadena[5];
    }
    else{
        var userRoom = cadena[5];
        var category = $('#category').data("id");
    }
    return {"category": category, "userRoom": userRoom};
}