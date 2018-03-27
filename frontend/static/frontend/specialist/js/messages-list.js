$(document).ready(function () {


    firebase.initializeApp(JSON.parse(apiEnvFirebase));

    // firebase.auth().signInAnonymously().catch(function (error) {
    //     var errorCode = error.code;
    //     var errorMessage = error.message;
    //     // ...
    // });
    var client_id = userID;
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
        var url_chat = $('.info-div').data('urlchat').replace('0',item.client)
        $("#list_categories").append("\
                        <a href='"+url_chat+"' class='list-group-item list-group-item-action cont' id='" + "cat" + item.key + "'>\
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
        // var fecha2 = moment(aux.date);
        // var fecha2 = ;
        // console.log("utc",moment(aux.date));
        // console.log("utc-5",fecha2.format('YYYYMMDD HHmmss'));
        // console.log("utc-5",moment(fecha2).tz("America/Toronto").format('Z'));
        // var fecha2 = moment(aux.date);
        // fecha de firebase en UTC-5
        // fecha2 = moment(fecha2).utcOffset("05:00");
        // var b = moment.duration(5, 'h');
        // console.log("test",fecha4.subtract(b));
        // fecha4 = fecha4.add(5, 'hours');
        // var fecha3 = moment(fecha2).add(-5, 'hours');
        // var date_utc = fecha2.add(5, 'hours');
        // var date_utc = moment().add(5, 'hours');
        // console.log("pre",fecha2);
        // var date_local = moment();
        // var diff = date_utc.diff(fecha2, 'hours');
        // var color = "green";
        // diff = 24 - diff;
        // if (diff < 4) {
        //     color = "red";
        //     // console.log(diff,"red");
        // }
        // else if (diff >= 4 && diff < 12) {
        //     color = "orange";
        //     // console.log(diff,"orange");
        // }
        // else if (diff >= 13 && diff <= 24) {
        //     color = "green";
        //     // console.log(diff,"green");
        // }
        // aux.clase = color;
        aux.message = aux.message.slice(0, 20) + ' ...';
        // aux.diff = diff;
        aux.date = dateTextCustom(moment.utc(aux.date), "-05:00");
        // aux.date = moment(fecha2).format('LT');

        //ver cuantos minutos pasaron desdedesde la ultima hora punta
        // var auxx = moment().startOf('hour').fromNow();
        // //obtener la hora de utc-5
        // var timestamp_utc_minus_5 = moment().utcOffset("-05:00");
        // var datetime = moment();
        // var aux5 = moment().diff(today12am, 'hours');


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
