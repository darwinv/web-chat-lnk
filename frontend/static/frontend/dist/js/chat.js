$(function() {

    $(".message").each(function(){
        var msg = $(this);
        var user_id = $('#user-id').data('user')
        if (msg.data("sender") != user_id){
            msg.removeClass("col-sm-offset-6 message")
            msg.addClass("message-answer")
            var bloq = msg.parent()
            // console.log("exito")
            bloq.after("<div class='arrow-down'>  </div>")
        }

    });

 var ws_scheme = window.location.protocol == "http:" ? "wss" : "ws";
//conformamos la url para conectar via ws
 api_url = apiUrl.replace("http","ws");
 //extraemos el id actual de usuario
 var user_id = $('#user-id').data('user');
 //extraemos la categoria
 var cadena = window.location.pathname.split("/");
 var category = cadena[5];
 // Nuestra sala, sera id usuario y id de especialidad
 var sala = user_id + '-' + category;
 var chatsock = new ReconnectingWebSocket(api_url + "/chat" + "/" + sala);

  chatsock.onopen = function open() {
  console.log('WebSockets connection created.');
};

 chatsock.onmessage = function(message) {
     var data = JSON.parse(message.data);
     // alert(message.data)

     var box_chat = $("#chat_box");
     $.each(data, function(key,value){
         var msg = value.message;
         var time = value.timeMessage;
         var codeUser = value.codeUser;


         var divMessage = "<div class='row globe-chat'>"+
                                "<div class='message col-sm-6 col-sm-offset-6' data-sender='"+value.user_id+"'>"+
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
             console.log(divMessage)
        box_chat.append(divMessage)

     });
     // console.log(data);
     // var chat = $("#chat")
     // var ele = $('<tr></tr>')
     //
     // ele.append(
     //     $("<td></td>").text(data.timestamp)
     // )
     // ele.append(s
     //     $("<td></td>").text(data.handle)
     // )
     // ele.append(
     //     $("<td></td>").text(data.message)
     // )
     //
     // chat.append(ele)
 };


 $("#chatform").on("submit", function(event) {
     var message = {
         title: $('#handle').val(),
         message: $('#message').val(),
         category: $("#chatform").data("category")
     }
     chatsock.send(JSON.stringify(message));
     $("#message").val('').focus();
     return false;
 });

 if (chatsock.readyState == WebSocket.OPEN) {
  chatsock.onopen();
}
});
