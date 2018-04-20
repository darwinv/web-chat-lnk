$(document).ready(function () {
    // Cargamos Firebase
    firebase.initializeApp(JSON.parse(apiEnvFirebase));
    console.log(apiEnvFirebase);
    var client_id = userID;
    console.log("id: "+client_id);
    // cargamos el listado de los mensajes de las especialidades
    var starCountRef = firebase.database().ref('categories/clients/u' + client_id).orderByChild('datetime');
    starCountRef.on('value', function (snapshot) {
            $("#list_categories").empty();
            var id_user = snapshot.key;
            inject_items(reverse_list(snapshot),id_user);
        });

   // cargamos el plan elegido
    var planObject = firebase.database().ref('chosenPlans/u' + client_id);
    planObject.on('value', function (snap){
      if (snap.exists()) {
        var plan = snap.val().plan_name;
        var available_queries = snap.val().available_queries;
        var query_quantity = snap.val().query_quantity;
        var expiration_date = snap.val().expiration_date;
        $("#chosen-plan").data("id", snap.val().id);
        $("#plan_name").text(plan);
        $("#queries").text(available_queries + '/'+ query_quantity);
        $("#expiration_date").text(expiration_date);
    }
    else{
      $("#chosen-plan").html(
        "<center> <button type='button' class='btn btn-md btn-ligth-blue cap' data-toggle='modal'"+
          "data-target='#reload'>"+ trans_reload+"</button> </center>");
    }

      // console.log(snap.val());
    });
    $("#chosen-plan").toggleClass("hidden");
}); // cierra document ready




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
                                        <img src='https://s3-sa-east-1.amazonaws.com/linkup-statics/arrows.png' class='image-cell'>\
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
