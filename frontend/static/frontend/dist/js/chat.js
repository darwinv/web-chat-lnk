$(function() {

changeMessage(); //se llama a la funcion change message
scrollDown(); // Scrolleamos hasta abajo
function changeMessage(){
    var previus_query_id = null
    $(".message").each(function(){
        var msg = $(this);
        var user_id = userID;
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

chatsock.onmessage = function(message) {
    const LIMIT_SCROLL = 1260;
    var data = JSON.parse(message.data);
    var audio = new Audio(audioNotification); //Inicializacion de audio
    var box_chat = $("#chat_box");
    $.each(data, function(key,value){
        var msg = value.message;
        var time = value.timeMessage;
        var codeUser = value.codeUser;

        // Se crea el div del globo para renderizarlo
        // debe validarse el tema de si soy el q cree el mensaje o al contrario
        var divMessage =   "<div class='row globe-chat'>"+
                                "<div class='cont-title-query' style='display: none'>"+
                                    "<div class='title-query'>"+
                                        value.query.title+
                                    "</div>"+
                                "</div>"+
                                "<div class='message col-sm-6 col-sm-offset-6'"+
                                "data-sender='"+value.user_id+"' data-query='"+value.query.id+"'>"+
                                    "<div class='row'>"+
                                        "<div class='col-sm-12'><p class='text'>"+value.message+"</p></div>"+
                                    "</div>"+
                                    "<div class='row'>"+
                                        "<div class='col-sm-6'>"+
                                            "<p class='code-user'>"+value.codeUser+"</p>"+
                                        "</div>"+
                                        "<div class='col-sm-6'>"+
                                            "<p><small class='time'>"+value.timeMessage+"</small></p>"+
                                        "</div>"+
                                    "</div>"+
                                "</div>"+
                            "</div>";
        box_chat.append(divMessage)
        // console.log("sender: "+ value.user_id + " conected: "+ userID);
        if (value.user_id != userID){
            audio.play();
        }
     });

    changeMessage();
    // Calculo la diferencia de pixeles entre el ultimo msj y el scroll
    var resta = $("#chat_box").scrollTop() - $("#chat_box .globe-chat:last").position().top;
    if (resta > LIMIT_SCROLL){
        scrollDown();
    }
    if (!$("#animacion").hasClass('hidden')){
        $("#animacion").addClass("hidden");
    }
};

$("#form-chat").submit(function(e){
    e.preventDefault();
    sendQueryMessage()
});


function sendQueryMessage(){
    text_message = $('#text_message').val();
    message_type = 'q';
    title_query = $('#title_query').val();
    query_id = "";

    // Validations
    if (text_message == "")
        return false;

    $("#animacion").toggleClass("hidden")

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
            content_type: "0",
            file_url: ""}],
        category: category,
        query: query_id
    }
    chatsock.send(JSON.stringify(message));

    $("#title_query").val('')
    $("#text_message").val('').focus();
    return false;
}

if (chatsock.readyState == WebSocket.OPEN) {
    chatsock.onopen();
}
});
