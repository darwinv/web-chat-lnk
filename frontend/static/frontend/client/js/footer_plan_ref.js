$(document).ready(function () {

    // firebase.initializeApp(JSON.parse(apiEnvFirebase));
    var client_id = userID;
  // cargamos el plan elegido
  planObject = firebase.database().ref('chosenPlans/u' + client_id);


  $.get( url_status_plan, function( data ) {
  
  });
  
//
// $('#reload').on('hidden.bs.modal', function () {
 planObject.on('value', function (snap){
     if (snap.exists()) {
       var available_queries = snap.val().available_queries;
       var query_quantity = snap.val().query_quantity;
       var expiration_date = snap.val().expiration_date;
       text = `<h4>${TRANS_QUERY_PLANS}</h4>
       <p id="plan_name">${snap.val().plan_name}</p>
       <p>${TRANS_AVAILABLES}:
         <span id="queries">${available_queries} / ${query_quantity}</span>
       </p>
       <p>${TRANS_EXPIRATION_DATE}:
         <span id="expiration_date">${expiration_date}</span></p><center>
         <button id="change_plan" type="button" class="btn btn-xs btn-ligth-blue cap"
        data-toggle="modal" data-target="#changePlan">${TRANS_CHANGE_PLAN}
        </button> </center> `;
         $("#chosen-plan").html(text);
     }
     else{
       $("#chosen-plan").html(
         "<center> <button type='button' class='btn btn-md btn-ligth-blue cap' data-toggle='modal'"+
           "data-target='#reload'>"+ TRANS_RELOAD +"</button> </center>");
       }
  });
   $("#chosen-plan").toggleClass('hidden');
// });

});
