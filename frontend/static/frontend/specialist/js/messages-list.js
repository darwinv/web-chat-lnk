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
    console.log("id: " + client_id);
    // if (!client_id == "None") {
    var starCountRef = firebase.database().ref('messageslist/specialist/s'+client_id).orderByChild('date');
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
        // console.log(item);
        $("#list_categories").append("\
                        <a href='#' class='list-group-item list-group-item-action cont' id='" + "cat" + item.key + "'>\
                            <div class='row '>\
                                <div class='col-10 cont'>\
                                        <div class='cont-item'>\
                                            <img src='" + itemVal.photo + "'class='rounded-circle itemp' id='img_cat'>\
                                            <p class='itemp'><strong class='nick'>" + itemVal.nick + "</strong>   <span class='date'>" + itemVal.date + "</span><br><span class='title'>" + itemVal.title + "</span><br><span class='" + itemVal.clase + "'>" + itemVal.message + "</span></p>\
                                        </div>\
                                </div>\
                                <div class='coll-2'>\
                                        <img src='https://s3-sa-east-1.amazonaws.com/linkup-statics/arrow.png' class='w'>\
                                </div>\
                            </div>\
                        </a>");
        cont += 1;
    });
}

function reverse_list(snapshot) {
    var l = new Array();
    snapshot.forEach(function (item) {
        var aux = item.val();
        var fecha2 = moment(aux.date).utc();
        var date_utc = moment().add(5, 'hours');
        var diff = date_utc.diff(fecha2, 'hours');
        var color = "green";
        diff = 24 - diff;
        if (diff < 4) {
            color = "red";
            // console.log(diff,"red");
        }
        else if (diff >= 4 && diff < 12) {
            color = "orange";
            // console.log(diff,"orange");
        }
        else if (diff >= 13 && diff <= 24) {
            color = "green";
            // console.log(diff,"green");
        }
        // aux.clase = color;
        aux.message = aux.message.slice(0, 20) + ' ...';
        aux.diff = diff;
        aux.date = moment(fecha2).format('LT');

//
//         }
        // var f=new Date();
        // cad=f.getFullYear()+"-"+f.getMonth()+"-"+f.getDay()+" "+f.getHours()+":"+f.getMinutes()+":"+f.getSeconds();
        //
        // fecha_2 = new Date(cad).getTime();
        // fecha_1 = new Date(aux.date).getTime();
        // delta = fecha_1-fecha_2;
        // console.log(fecha_1);
        // console.log(fecha_2);
        // console.log(delta/(1000*60*60*24));
        // console.log(f);
        // console.log(cad);
        // console.log(item.val());
        // console.log(aux);
        l.push(aux);
        // l.push(item.val());
    });
    return l;
}