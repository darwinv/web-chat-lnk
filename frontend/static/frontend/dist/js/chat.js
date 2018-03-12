$(function() {

// cambiar posicion de mensaje de Chat
// if $(".message").data("typemessage") == 'a'{
//
// }
$(".message").each(function(){
    var msg = $(this);
    var user_id = $('#user-id').data('user')
    if (msg.data("sender") != user_id){
        msg.removeClass("col-sm-offset-6 message")
        msg.addClass("message-answer")
    }
  });
});
