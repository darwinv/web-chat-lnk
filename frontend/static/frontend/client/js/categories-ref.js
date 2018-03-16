$(document).ready(function () {
    //credenciales db marko
    // var config = {
    //     apiKey: "AIzaSyB804F8eGGoUg_HThtuJT9o80gAapjNV0k",
    //     authDomain: "test-72ce0.firebaseapp.com",
    //     databaseURL: "https://test-72ce0.firebaseio.com",
    //     projectId: "test-72ce0",
    //     storageBucket: "test-72ce0.appspot.com",
    //     messagingSenderId: "781009340958"
    // };

    //credenciales db linkup
    config = {
        "apiKey": "AIzaSyDoYMhNo1RP1JYrQN1pX84w4YL82N7MURM",
        "authDomain": "linkup-5b6f4.firebaseapp.com",
        "databaseURL": "https://linkup-5b6f4.firebaseio.com",
        "projectId": "linkup-5b6f4",
        "storageBucket": "linkup-5b6f4.appspot.com"
    };
    firebase.initializeApp(config);

    // firebase.auth().signInAnonymously().catch(function (error) {
    //     var errorCode = error.code;
    //     var errorMessage = error.message;
    //     // ...
    // });
    var client_id = $('#client_id').text();
    console.log("id: "+client_id);
    // if (!client_id == "None") {
        var starCountRef = firebase.database().ref('categories/clients/u' + client_id).orderByChild('datetime');
        starCountRef.on('value', function (snapshot) {
            $("#list_categories").empty();
            // $("#lista_cats").remove();
            inject_items(reverse_list(snapshot));

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

function inject_items(list_items) {
    var cont = 0;
    list_items.forEach(function (item) {
        var itemVal = item;
        // console.log(item)/
        // chat = 'es/web/client/chat/'
        var url_chat = $('#client_id').data('urlchat').replace('0',item.id)
        $("#list_categories").append("\
                        <a href='"+url_chat+"' class='list-group-item list-group-item-action cont'  id='" + "cat" + item.id + "'>\
                            <div class='row'>\
                                <div class='col-10'>\
                                    <div class='row'>\
                                        <div class='cont-item'>\
                                            <img src='" + itemVal.image + "'class='rounded-circle itemp' id='img_cat'>\
                                            <span class='itemp'>" + itemVal.name + "</span>\
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
        l.push(item.val());
    });
    return l.reverse();
}
