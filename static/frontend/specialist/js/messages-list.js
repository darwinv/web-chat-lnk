/*CARGAR DATA EN EL LISTADO DE CLIENTES*/
$(document).ready(function () {
    firebase.initializeApp(JSON.parse(apiEnvFirebase));
    var client_id = userID;
    var starCountRef = firebase.database().ref(
        'messagesList/specialist/s'+client_id).orderByChild('date');
    starCountRef.on('value', function (snapshot) {
        $("#list_categories").empty();
        inject_items(reverse_list(snapshot));
    });
});
function reverse_list(snapshot) {
    var l = new Array();    
    snapshot.forEach(function (item) {
        var aux = item.val();
        aux.queryCurrent.message = aux.queryCurrent.message.slice(
                                0, 20) + ' ...';
        aux.queryCurrent.date = dateTextCustom(
                                moment.utc(aux.queryCurrent.date), "-05:00");
        l.push(aux);
    });
    return l;
}
function inject_items(list_items) {
    var cont = 0;
    cell = `<li 
             class='manage-query-specialist'
              data-pending-query='{pendingQuery}' data-query-id='{queryId}'
                data-client-id='{clientId}'>
                <div class='list-group-item list-group-item-action pull-left'>
                    <div class='col-xs-9 cont'>
                        <div class='cont-item'>
                            <img src='{photo}' class='rounded-circle itemp' 
                            id='img_cat'>
                            <p class='itemp'>
                                <strong class='nick'>{displayName}</strong>
                                <span class='title'>{title}</span><br>
                                <span>{message}</span>
                            </p>
                        </div>
                    </div>
                    <div class='col-xs-3 text-right'>
                        <span class='date size10'>{date}</span><br>
                        {pendingQueries}
                        {pendingQueriesToSolve}
                    </div>
                </div>
                {ul}
            </li>`;                        

    list_items.forEach(function (item) {
        var itemVal = item;
        var countPendings = 0;
        var toogleTree = pendingQueries = queryId = pendingQueriesToSolve = ""
        for (var key in itemVal.queries) {
            // skip loop if the property is from prototype
            if (!itemVal.queries.hasOwnProperty(key)) continue;

            var obj = itemVal.queries[key];
                       
            toogleTree = toogleTree + cell.format_hard({
                        "pendingQuery": "1",
                        "photo": itemVal.photo,
                        "displayName": itemVal.displayName,
                        "date": dateTextCustom(moment.utc(obj.date), "-05:00"),
                        "title": obj.title,
                        "message": obj.message,
                        "pendingQueries": `<span class='number-circule 
                                            circule-pink'>1<span>`,
                        "pendingQueriesToSolve": "",
                        "ul": "",
                        "queryId": obj.id,
                        "clientId": itemVal.client
                    });
            countPendings++
        }

        if (countPendings > 1) {
            // Si se necesita desplegar queries
            toogleTree = `<ul class='tree' style='display:none'>
                            ${toogleTree}</ul>`
            pendingQueries = `<span class='number-circule circule-pink'>
                            ${countPendings}</span>`
            queryId = obj.id
        }else if (countPendings > 0) {
            // Mostrar los queries pendientes si queries > 0 < 2
            pendingQueries = `<span class='number-circule circule-pink'>
                            ${countPendings}</span>`
            queryId = obj.id
            toogleTree = ""
        }

        if (itemVal.pending_queries_to_solve > 0) {
            pendingQueriesToSolve = `<span 
                                    class='number-circule circule-turque'>
                                    ${itemVal.pending_queries_to_solve}</span>`
        }

        var t = cell.format_hard({
                        "pendingQuery": countPendings,
                        "photo": itemVal.photo,
                        "displayName": itemVal.displayName,
                        "date": itemVal.queryCurrent.date,
                        "title": itemVal.queryCurrent.title,
                        "message": itemVal.queryCurrent.message,
                        "pendingQueries": pendingQueries,
                        "pendingQueriesToSolve": pendingQueriesToSolve,
                        "ul": toogleTree,
                        "queryId": queryId,
                        "clientId": itemVal.client
                    });
        
        $("#list_categories").append(t)
    });
}

$(document).on('click','.manage-query-specialist',function(){
    /* Manejar listado de clientes */
    pending_queries = $(this).data("pending-query")
    queryId = $(this).data("query-id")
    clientId = $(this).data("client-id")
    if (pending_queries > 1) {
        /*Desplegar consultas*/
        $(this).children('ul.tree').toggle();
    }else if(pending_queries == 1){
        /*Mostrar Modal*/
        loadModalQueryData(queryId, clientId)
        $('#manage_query_specialist').modal('show'); 
    }else{
        /*llevame al chat*/        
        url = CHAT_SPECIALIST.replace('0', $(this).data("client-id"));
        window.location.href = url;
    }
});
function loadModalQueryData(queryId, clientId){
    /*gestionar la carga del query en el modal*/
    // Contenedor listado
    var win = $("#manage_query_specialist").find('#modal_content_list');
    win.data("query-id",queryId)
    win.data("client-id",clientId)
    win.data("url",'queries-messages/{}/'.format(queryId));  // Url a consumir
    win.data("lastScrollTop", -1) // Inicializamos variable Top solo Modales
    DoAjaxToModalQueryData(win);
    $("#manage_query_specialist").find("button").removeAttr("disabled");
}


/*ACEPTAR QUERY*/
$(document).on('submit','#manage_query_modal',function(event){
    /*Usuario acepta el query*/
    event.preventDefault();
    var win = $("#manage_query_specialist").find('#modal_content_list');
    data = {
        "url": `query-accept/${win.data("query-id")}`,
    }
    
    $("#manage_query_specialist").find("button").attr("disabled", true);
    sendAjaxService(data, function(response) {
        // go to chat
        url = CHAT_SPECIALIST.replace('0', win.data("client-id"));
        window.location.href = url;
    }, type="PUT")

});


/*BOTONES DE DERIVAR QUERY*/
$(document).on('click','.derive-query',function(event){
    /*Usuario le da click boton deriva*/
    event.preventDefault();
    showModalDeriveDecline();
}); 
$(document).on('click','.derive-associate-list .rounded-circle',function(event){
    /*Usuario deriba o declina*/
    if($(this).siblings("input").is(':enabled')) {
        $(".derive-associate-list").find("associate-radio").prop("checked", true);
        $(this).siblings("input").prop("checked", true);

        $("#derive-query").removeAttr("disabled");
    }
});

$('#manage_query_specialist').on('hidden.bs.modal', function () {
    /*al ocultar el modal de derivar*/
    $(".container-modal-inputs").empty();
});
$(document).on('submit','#derive_query_modal',function(event){
    /*Usuario deriva el query*/
    event.preventDefault();
    specialist = $('input[name=associate-radio]:checked').val();
    var win = $("#derive_query_specialist").find('#modal_content_list');

    data = {
        "url": `query-derive/${win.data("parameters").query}`,
        "specialist": specialist
    }
    
    $("#derive-query").attr("disabled", true);
    sendAjaxService(data, function(response) {
        $('#derive_query_specialist').modal('hide');
        $("#derive-query").removeAttr("disabled");
    }, type="PUT")
});
function loadModalAsociateData(queryId){
    /*gestionar la carga de ASOCIADOS en el modal*/
    // Contenedor listado
    var win = $("#derive_query_specialist").find('#modal_content_list');
    parameters = {'query': queryId}
    win.data("parameters", parameters);
    win.data("url",'specialists-asociate/');  // Url a consumir
    win.data("lastScrollTop", -1); // Inicializamos variable Top solo Modales
    DoAjaxToModalAsociateSpecialistsData(win);
}


/*BOTONES DE DECLINAR QUERY*/
$(document).on('click','.decline-query',function(event){
    /*Usuario le da click boton declina*/
    event.preventDefault();
    showModalDeriveDecline();
});
$(document).on('submit','#decline_query_modal',function(event){
    /*Usuario acepta el query*/
    event.preventDefault();
    message = $('#message_decline').val();
    var win = $("#manage_query_specialist").find('#modal_content_list');
    data = {
        "url": `query-decline/${win.data("query-id")}`,
        "message": message
    }
    $("#decline-query").attr("disabled", true);
    sendAjaxService(data, function(response) {       
        $('#decline_query_specialist').modal('hide');
        $("#decline-query").removeAttr("disabled");
    }, type="PUT")

});


function showModalDeriveDecline(){
    if (type_specialist=="m") {
        // Contenedor listado
        var win = $("#manage_query_specialist").find('#modal_content_list');
        loadModalAsociateData(win.data("query-id"));
        $('#manage_query_specialist').modal('hide');
        $('#derive_query_specialist').modal('show');
    }else{
        $('#manage_query_specialist').modal('hide');
        $('#decline_query_specialist').modal('show');
    }
}

/*FUNCIONES GET AJAX*/
function DoAjaxToModalQueryData(win){
    win.sendAjaxPagination(function(data) {
        htmlMessage = ""
        $(".modal-body .header-modal").find(".rounded-circle").attr("src",data.user.photo)
        $(".modal-body .header-modal").find(".nick").html(data.user.display_name)
        $(".modal-body").find(".title-modal").html(data.title)

        cell = "<div>{message}</div>"
        for (var key in data.message) {
            // skip loop if the property is from prototype
            if (!data.message.hasOwnProperty(key)) continue;

            var obj = data.message[key];
            if (obj.content_type == 1) {
                htmlMessage = htmlMessage + cell.format_hard({
                    "message":obj.message
                })
            }
        }
        win.find(".mensages-list").html(htmlMessage)

        win.show();
        if (type_specialist=="m") {
            $('#manage_query_specialist').find('.derive-query').show();
        }else{
            $('#manage_query_specialist').find('.decline-query').show();
        }        
    });
}
function DoAjaxToModalAsociateSpecialistsData(win){
    win.sendAjaxPagination(function(data) {
        html_specialist = "";
        count_associates = 0;
        cell = `<div class='cont-item user-chat-logo'>
                    <input {declined} type='radio' name='associate-radio'
                     value='{id}' />
                    <img src='{photo}' data-specialist-id='{id}'
                    class='rounded-circle itemp'  title='{name}'>
                </div>`;

        for (var key in data) {
            declined = ""
            // skip loop if the property is from prototype
            if (!data.hasOwnProperty(key)) continue;
            var obj = data[key];

            if (obj.declined) {
                declined = "disabled"
            }
            
            html_specialist = html_specialist + cell.format_hard({
                "photo":obj.photo,
                "id": obj.id,
                "name": `${obj.last_name} ${obj.first_name}`,
                "declined": declined
            })
            count_associates++;
        }
        win.find(".derive-associate-list").html(html_specialist)
    });
}