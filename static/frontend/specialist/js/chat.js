$(function() {
    $("#selection_message_alert").show();
    $(".send-message-cont").hide();
});

$(document).on('click', ".close-reply", function(){
    $("#reply-content").data("message-reference", null).hide();
    $("#selection_message_alert").show();
    $(".send-message-cont").hide();
    $(".fileinput-remove").click();    
});