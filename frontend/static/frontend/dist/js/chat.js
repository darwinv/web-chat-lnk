$(function() {

changeMessage(); //se llama a la funcion change message
if ($('#chat_box .globe-chat').length) {
  scrollDown(); // si existe al menos uno  Scrolleamos hasta abajo
}

function changeMessage(){
    var previus_query_id = null

    $(".message").each(function(){
        var msg = $(this);
        var user_id = userID;
        // Renderizamos el time en el listado
        var timeMessage = msg.data("timemessage");
        timeMessage = toLocalTime(timeMessage);
        msg.find("small.time").text(timeMessage)
        if (msg.data("sender") != user_id){
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

function scrollDown(){
    var ultimo = $("#chat_box .globe-chat:last").position().top;
    var scrollchat = $("#chat_box").scrollTop();
    $("#chat_box").animate({scrollTop:ultimo+scrollchat});
}

var ws_scheme = window.location.protocol == "http:" ? "wss" : "ws";
//conformamos la url para conectar via ws
api_url = apiUrl.replace("http","ws");
// Comparamos los roles para que se conecten a la sala como corresponde
role_id = roleID;
var cadena = window.location.pathname.split("/");
if (role_id == ROLES.client){
    //extraemos el id actual de usuario
    var user_id = userID
    //extraemos la categoria
    var category = cadena[5];
}
else{
    var user_id = cadena[5];
    var category = $('#category').data("id");
}
// Nuestra sala, sera id usuario y id de especialidad
var room = user_id + '-' + category;
var chatsock = new ReconnectingWebSocket(api_url + "/chat" + "/" + room);

chatsock.onopen = function open() {
    console.log('WebSockets connection created.');
};

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

chatsock.onmessage = function(message) {
    var audio = new Audio(audioNotification);
    var data = JSON.parse(message.data);
    var boxChat = $("#chat_box");
    var chat_box = document.getElementById("chat_box");
    var positionScroll = chat_box.scrollTop;
    var diffScroll = chat_box.scrollHeight - chat_box.clientHeight;
    var resScroll = positionScroll / diffScroll;
    $.each(data, function(key,value){
        var msg = value.message;
        console.log(value.id);
        var codeUser = value.codeUser;
        // Se crea el div del globo para renderizarlo
        // se valida el tema de si soy el q cree el mensaje o al contrario
        var divMessage = "<div id='message_'"+value.id+"' class='row globe-chat'>"+
                                "<div class='cont-title-query' style='display: none'>"+
                                    "<div class='title-query'>"+
                                        value.query.title+
                                    "</div>"+
                                "</div>"+
                                "<div class='message col-sm-6 col-sm-offset-6'"+
                                "data-sender='"+value.user_id+"' data-timemessage='"+value.timeMessage+"' data-query='"+value.query.id+"'>"+
                                    "<div class='row'>"+
                                        "<div class='col-sm-12'><p class='text'>"+value.message+"</p></div>"+
                                    "</div>"+
                                    "<div class='row'>"+
                                        "<div class='col-sm-6'>"+
                                            "<p class='code-user'>"+value.codeUser+"</p>"+
                                        "</div>"+
                                        "<div class='col-sm-6'>"+
                                            "<p><small class='time'></small></p>"+
                                        "</div>"+
                                    "</div>"+
                                "</div>"+
                            "</div>";
        boxChat.append(divMessage)
        // console.log("sender: "+ value.user_id + " conected: "+ userID);
        if (value.user_id != userID){
            audio.play();
        }
     });

    changeMessage();
    // Calculo la diferencia de pixeles entre el ultimo msj y el scroll
    // var resta = $("#chat_box").scrollTop() - $("#chat_box .globe-chat:last").position().top;
    if (resScroll >= 0.9){
        scrollDown();
    }
    if (!$("#animacion").hasClass('hidden')){
      console.log("en scrollwdown");
        $("#animacion").addClass("hidden");
    }
};

$("#form-chat").submit(function(e){
    e.preventDefault();
    //sendQueryMessage()
    $("#animacion").toggleClass("hidden");
    var text_message = $('#text_message').val();
    var message_type = 'q';
    var title_query = $('#title_query').val();
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    var files = $('#file-linkup').fileinput('getFileStack');
    var url_send_query = $(this).data('queryurl');
    var arr_files = []

    for (i = 0; i < files.length; i++) {
        arr_files[i] = {
          name: files[i].name,
          type: files[i].type
        }
     }

    var message = {
      title: title_query,
      message_text: {
            message: text_message,
            msg_type: message_type,
            content_type: 1,
            file_url: ''
          },
        category: category
    };

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
        type:"POST",
        url:url_send_query,
        data: {
          query_data:JSON.stringify(message),
          files:JSON.stringify(arr_files)
        },
        success: function(data){
          console.log("en callback");
          $("#title_query").val('');
          $("#text_message").val('').focus();
          console.log(data);
          fetchData(data.query_id, data.message_files_id)
          $('#file-linkup').fileinput('upload');
        }
   });

});

function fetchData(query_id, msgs){

  $('#file-filepreajax').on('filepreupload', function(event, data, previewId, index) {
    data.extra = { 'query': query_id, 'messages':msgs }
    console.log(data);
    // return data;
  });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendQueryMessage(){
    text_message = $('#text_message').val();
    message_type = 'q';
    title_query = $('#title_query').val();
    query_id = "";

    // Validations
    if (text_message == "")
        return false;
    console.log("send query message")
    $("#animacion").toggleClass("hidden");

    if (role_id == ROLES.specialist) {
        message_type = 'a';
        title_query = "";
        category = "";
        query_id = $("#chat_box div.message-left:last").data("query");
    }

    var message = {
        token : token,
        title: title_query,
        message:[{
            message: text_message,
            msg_type: message_type,
            content_type: "1",
            file_url: ""}],
        category: category,
        query: query_id
    }
    console.log(chatsock.send(JSON.stringify(message)));

    $("#title_query").val('')
    $("#text_message").val('').focus();
    return false;
}

if (chatsock.readyState == WebSocket.OPEN) {
    chatsock.onopen();
}
});
