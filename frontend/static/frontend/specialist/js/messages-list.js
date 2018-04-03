$(document).ready(function () {

    firebase.initializeApp(JSON.parse(apiEnvFirebase));
    var itemVal = item;
    var client_id = userID;
    console.log("id: " + client_id);
    var starCountRef = firebase.database().ref('messageslist/specialist/s'+client_id).orderByChild('date');
    starCountRef.on('value', function (snapshot) {
        $("#list_categories").empty();
        inject_items(reverse_list(snapshot));
    });
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
                                        <img src='https://s3-sa-east-1.amazonaws.com/linkup-statics/arrow.png' class='image-cell'>\
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
        aux.message = aux.message.slice(0, 20) + ' ...';
        aux.date = dateTextCustom(moment.utc(aux.date), "-05:00");

        l.push(aux);

    });

    return l;
}
