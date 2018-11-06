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
    var audio = new Audio(audioNotification);
    var data = JSON.parse(message.data);
    var boxChat = $("#chat_box");
    var chat_box = document.getElementById("chat_box");
    var positionScroll = chat_box.scrollTop;
    var diffScroll = chat_box.scrollHeight - chat_box.clientHeight;
    var resScroll = positionScroll / diffScroll;
    
    $.each(data.messages, function(key,value){
        var msg = value.message;
        var codeUser = value.codeUser;
        // Se crea el div del globo para renderizarlo
        // se valida el tema de si soy el q cree el mensaje o al contrario
        var divMessage = `<div id='message_'${value.id}' class='row globe-chat'>
                                <div class='cont-title-query' 
                                style='display: none'>
                                    <div class='title-query'>
                                        ${data.query}
                                    </div>
                                </div>
                                <div class='message col-sm-6 col-sm-offset-6'
                                data-sender='${value.user_id}' 
                                data-timemessage='${value.timeMessage}' 
                                data-query='${value.query_id}'>
                                    <div class='row'>
                                        <div class='col-sm-12'>
                                            <p class='text'>
                                                ${value.message}
                                            </p>
                                        </div>
                                    </div>
                                    <div class='row'>
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
};
if (chatsock.readyState == WebSocket.OPEN) {
    chatsock.onopen();
}

$("#form-chat").submit(function(e){
    e.preventDefault();
    //sendQueryMessage()
    $("#animacion").toggleClass("hidden");
    var title_query = $('#title_query').val();
    var textMessage = $('#text_message').val();
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    var messageType = 'q';
    var files = $('#file-linkup').fileinput('getFileStack');
    
    var arr_files = []

    var dataQuery = {
        title: title_query,
        category: category,
        message: [{
            msg_type: messageType,
            message: textMessage,
            content_type: 1,
            file_url: ''
        }],
    };

    var date = new Date();
    datestring = date.yyyymmdd();
    for (i = 0; i < files.length; i++) {

        if (files[i].type == 'Image'){
            prefixFile = "IMG";
            contentType = 2;
        }
        else if (files[i].type == 'Video'){
            prefixFile = "VID";
            contentType = 3;
        }
        else if (files[i].type == 'Voice'){
            prefixFile = "AUD";
            contentType = 4;
        }
        else if (files[i].type == 'Document'){
            prefixFile = "DOC";
            contentType = 5;
        }else{
            prefixFile = "NONE";
            contentType = 5;
        }
        file_url = `${prefixFile}-${datestring}-22222.${files[i].extension}`;
        arr_files[i] = {
            msg_type: messageType,
            message: '',            
            content_type: contentType,
            file_url: file_url
        }        
    }
    
    dataQuery["message"] = dataQuery["message"].concat(arr_files);
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
        url: url_send_query,
        data: {
            query_data:JSON.stringify(dataQuery)
        },
        success: function(data){
            console.log(data);
            $("#title_query").val('');
            $("#text_message").val('').focus();
            fetchData(data.query_id, data.message_files_id)
            // $('#file-linkup').fileinput('upload');
            if (!$("#animacion").hasClass('hidden')){
                $("#animacion").addClass("hidden");
            }
            
        }
   });

});

function sendFilesMessages(query){
    data = {
        "url": `queries/upload_files/${query}/`,
        "file": JSON.stringify(files),
    }
    sendAjaxService(data, function(response){
        console.log("response ajax");
    }, "PUT");
    console.log("HAMBREEEEEEEEEEE");
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
function fetchData(query_id, msgs){
  $('#file-filepreajax').on('filepreupload', function(
    event, data, previewId, index) {
    data.extra = { 'query': query_id, 'messages':msgs }
  });
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
function updateMessage(){
    // Mostrar un solo titulo por grupo de query
    var previus_query_id = null

    $(".message").each(function(){
        var msg = $(this);
        // Renderizamos el time en el listado
        var timeMessage = msg.data("timemessage");
        timeMessage = toLocalTime(timeMessage);
        msg.find("small.time").text(timeMessage)
        if (msg.data("sender") != userID){
            msg.removeClass("col-sm-offset-6");
            msg.addClass("message-left");
        }else{
            msg.addClass("message-right");
        }

        if (msg.data("query") != previus_query_id){
            msg.siblings(".cont-title-query").show();
            previus_query_id = msg.data("query");
        }else{
            msg.siblings(".cont-title-query").remove();
        }

    });
}
Date.prototype.yyyymmdd = function() {
  var mm = this.getMonth() + 1; // getMonth() is zero-based
  var dd = this.getDate();

  return [this.getFullYear(),
          (mm>9 ? '' : '0') + mm,
          (dd>9 ? '' : '0') + dd
         ].join('');
};
});
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