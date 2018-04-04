$(document).ready(function () {

//     $(".e").on("click", function(){
//         console.log("pasee1");
// }); $(".e img").on("click", function(){
//         console.log("pasee2");
// }); $(".cont-item").on("click", function(){
//         console.log("pasee3");
// }); $(".itemp").on("click", function(){
//         console.log("pasee4");
// }); $(".info-div").on("click", function(){
//         console.log("pasee5");
// });

    firebase.initializeApp(JSON.parse(apiEnvFirebase));
    console.log(apiEnvFirebase);
    // firebase.auth().signInAnonymously().catch(function (error) {
    //     var errorCode = error.code;
    //     var errorMessage = error.message;
    //     // ...
    // });
    var client_id = userID;
    console.log("id: "+client_id);
    // if (!client_id == "None") {
        var starCountRef = firebase.database().ref('categories/clients/u' + client_id).orderByChild('datetime');
        starCountRef.on('value', function (snapshot) {
            $("#list_categories").empty();
            // $("#lista_cats").remove();
            var id_user = snapshot.key;
            // console.log(id_user);
            inject_items(reverse_list(snapshot),id_user);
            // snapshot.forEach(function (item) {
            //     var itemVal = item.val();
            //     if ($("#cat" + item.key).length) {
            //         $("#cat" + item.key).replaceWith("<a href='#' class='list-group-item justify-content-between list-group-item-action' id='" + "cat" + item.key + "'>" + "<img src='" + itemVal.image + "' class='rounded-circle'>" + itemVal.name + "<img src='https://s3.amazonaws.com/linkup-photos/82cffad1-e6f8-4f75-a711-a33c3f272131.png' class=''></a>");
            //     }
            //     else {
            //         $("#list_categories").append("\
            //                 <a href='#' class='list-group-item list-group-item-action' id='" + "cat" + item.key + "'>\
            //                     <div class='row'>\
            //                         <div class='col-4'>\
            //                             <img src='" + itemVal.image + "'\
            //                                  class='rounded-circle' id='img_cat'>\
            //                         </div>\
            //                         <div class='col-4' id=''>\
            //                             <span>" + itemVal.name + "</span>\
            //                         </div>\
            //                         <div class='col-2 offset-2'>\
            //                             <img src='https://s3.amazonaws.com/linkup-photos/82cffad1-e6f8-4f75-a711-a33c3f272131.png' class=''>\
            //                         </div>\
            //                     </div>\
            //                 </a>");
            //         // $("#list_categories").append("<a href='#' class='list-group-item justify-content-between list-group-item-action' id='" + "cat" + item.key + "'>" + "<img src='" + itemVal.image + "' class='rounded-circle'>" + itemVal.name + "<img src='https://s3.amazonaws.com/linkup-photos/82cffad1-e6f8-4f75-a711-a33c3f272131.png' class=''></a>");
            //     }
            // });
        });
    // }
});
function putViewToApi(p_1, p_2) {
    console.log(p_1,p_2);
    $.ajax({
    url: "http://192.168.1.8:9000/message-view/",
    type: 'PUT',
        success: function(data) {
        console.log(data);
    },
    data: {
	"id_user": 11,
	"category":8
}
  });
    return "ddd";
}

function inject_items(list_items,  id_user) {
    var cont = 0;
    list_items.forEach(function (item) {
        var itemVal = item;
        // chat = 'es/web/client/chat/'
        console.log(itemVal.datetime);
        var url_chat = $('.info-div').data('urlchat').replace('0',item.id);
        $("#list_categories").append("\
                        <a href='"+url_chat+"' class='list-group-item list-group-item-action cont' onclick=\"return putViewToApi('"+id_user+"',"+item.id+");\"id='" + "cat" + item.id + "'>\
                            <div class='row'>\
                                <div class='col-10'>\
                                    <div class='row'>\
                                        <div class='cont-item'>\
                                            <img src='" + itemVal.image + "'class='rounded-circle itemp' id='img_cat'>\
                                            <div class='itemp'><strong>" + itemVal.name +"</strong><br>"+itemVal.datetime+"</div>\
                                        </div>\
                                     </div>\
                                </div>\
                                <div class='col-2 e'>\
                                        <img src='https://s3-sa-east-1.amazonaws.com/linkup-statics/arrows.png' class='w'>\
                                </div>\
                            </div>\
                        </a>");
        cont += 1;
    });
}
function reverse_list(snapshot) {
    var l = new Array();
    snapshot.forEach(function (item) {
        if(item.val().datetime){
            var aux = item.val();
            aux.datetime = dateTextCustom(moment.utc(item.val().datetime), "-05:00");
            l.push(aux);
        }
        else{
            l.push(item.val());
        }
    });
    return l.reverse();
}
