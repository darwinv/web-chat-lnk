$(document).ready(function () {

    firebase.initializeApp(JSON.parse(apiEnvFirebase));

    var client_id = userID;
    var starCountRef = firebase.database().ref('messagesList/specialist/s'+client_id).orderByChild('date');
    starCountRef.on('value', function (snapshot) {
        $("#list_categories").empty();
        inject_items(reverse_list(snapshot));
    });
});

function inject_items(list_items) {
    var cont = 0;

    cell = "<li \
             class='manage-query-specialist'\
              data-pending-query='{pendingQuery}'>\
                <div class='list-group-item list-group-item-action pull-left'>\
                    <div class='col-xs-9 cont'>\
                        <div class='cont-item'>\
                            <img src='{photo}'class='rounded-circle itemp' id='img_cat'>\
                            <p class='itemp'><strong class='nick'>{displayName}</strong>\
                               <span class='title'>{title}</span><br>\
                               <span>{message}</span>\
                            </p>\
                        </div>\
                    </div>\
                    <div class='col-xs-3 text-right'>\
                        <span class='date size10'>{date}</span><br>\
                        {pending_queries}\
                        {pending_queries_to_solve}\
                    </div>\
                </div>\
                {ul}\
            </li>";

                        

    list_items.forEach(function (item) {
        var itemVal = item;
        var count_pendings = 0;
        var toogle_tree = ""
        for (var key in itemVal.queries) {
            // skip loop if the property is from prototype
            if (!itemVal.queries.hasOwnProperty(key)) continue;

            var obj = itemVal.queries[key];
                       
            toogle_tree = toogle_tree + cell.format_hard({
                        "pendingQuery": "1",
                        "photo": itemVal.photo,
                        "displayName": itemVal.displayName,
                        "date": dateTextCustom(moment.utc(obj.date), "-05:00"),
                        "title": obj.title,
                        "message": obj.message,
                        "pending_queries": "<span class='number-circule circule-pink'>{}<span>".format(1),
                        "pending_queries_to_solve": "",
                        "ul": ""
                    });
            count_pendings++
        }

        if (count_pendings > 1) {
            toogle_tree = "<ul class='tree' style='display:none'>{}</ul>".format(toogle_tree)
        }else{
            toogle_tree = ""
            //toogle_tree = "<ul >{}</ul>".format(toogle_tree)
        }

        if (count_pendings > 0) {
            pending_queries = "<span class='number-circule circule-pink'>{}</span>".format(count_pendings)
        }else{
            pending_queries = ""
        }
        if (itemVal.pending_queries_to_solve > 0) {
            pending_queries_to_solve = "<span class='number-circule circule-turque'>\
            {}</span>".format(itemVal.pending_queries_to_solve)
        }else{
            pending_queries_to_solve = ""
        }
        var t = cell.format_hard({
                        "pendingQuery": count_pendings,
                        "photo": itemVal.photo,
                        "displayName": itemVal.displayName,
                        "date": itemVal.queryCurrent.date,
                        "title": obj.title,
                        "message": obj.message,
                        "pending_queries": pending_queries,
                        "pending_queries_to_solve": pending_queries_to_solve,
                        "ul": toogle_tree
                    });
        
        $("#list_categories").append(t)
    });
}

function reverse_list(snapshot) {
    var l = new Array();
    // console.log(snapshot)
    snapshot.forEach(function (item) {
      // console.log(item.val());
        var aux = item.val();
        // console.log(aux.queryCurrent.message);
        aux.queryCurrent.message = aux.queryCurrent.message.slice(0, 20) + ' ...';
        aux.queryCurrent.date = dateTextCustom(moment.utc(aux.queryCurrent.date), "-05:00");
        l.push(aux);
    });
    return l;
}

$(document).on('click','.manage-query-specialist',function(){
    pending_queries = $(this).data("pending-query")
    console.log(pending_queries)
    if (pending_queries > 1) {
        $(this).children('ul.tree').toggle();
    }else if(pending_queries == 1){
        $('#manage_query_specialist').modal('show');
    }else{
        //llevame al chat
    }    
});


var query = new Object();
$('#manage_query_specialist').on('shown.bs.modal', function (e) {
    // Cuando abre vista modal de los planes
    var win = $('#modal_content_list'); // Contenedor listado   
    //Inicializando data 
    win.data("url",'queries-messages/'.concat("25/"));  // Url a consumir
    loadModalQueryData(win);
});
function loadModalQueryData(win){
    console.log(win.data("url"))
    win.sendAjaxPagination(null, function(data) {
        query = data
        console.log(query)
    });
}
$('#manage_query_specialist').on('hidden.bs.modal', function () {
    $(".container-modal-inputs").empty();
    $("#message").empty();
    $("#message").removeClass();
});