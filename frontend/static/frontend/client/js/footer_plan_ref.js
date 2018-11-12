$(document).ready(function () {

    // firebase.initializeApp(JSON.parse(apiEnvFirebase));
    var client_id = userID;
  // cargamos el plan elegido
  planObject = firebase.database().ref('chosenPlans/u' + client_id);




//
// $('#reload').on('hidden.bs.modal', function () {
 planObject.on('value', function (snap){
    $.get( url_status_plan, function( data ) {
        console.log(data); 
      
      if (snap.exists()) {
        
          var available_queries = snap.val().available_queries;
          var query_quantity = snap.val().query_quantity;
          var expiration_date = snap.val().expiration_date;
          
          text1 = `<h4>${TRANS_QUERY_PLANS}</h4>
                  <p id="plan_name">${snap.val().plan_name}</p>
                  <p>${TRANS_AVAILABLES}:
                  <span id="queries">${available_queries} / ${query_quantity}</span></p>
                  <p>${TRANS_EXPIRATION_DATE}:
                  <span id="expiration_date">${expiration_date}</span></p>`;
          
          buttonChangePlan = `<center> <button id="change_plan" type="button" class="btn btn-xs btn-ligth-blue cap"
                        data-toggle="modal" data-target="#changePlan">${TRANS_CHANGE_PLAN}</button> 
                        </center>`;
          
          buttonReload = `<center> <button type='button' class='btn btn-md btn-ligth-blue cap' data-toggle='modal'"
          "data-target='#reload'>"${TRANS_RELOAD}"</button> </center>`;

          finalText = text1 + buttonChangePlan;              
          if(data.code == 5) {
             textExpired = `<p class='warning-plan'> Su plan Seleccionado ha expirado</p>`;
             finalText = text1 + textExpired + buttonReload;
          }
          if (data.code == 6) {
             textExpired = `<p class='warning-plan'> Su plan Seleccionado ha expirado, seleccione otro</p>`;
             finalText = text1 + textExpired + buttonChangePlan;
          }
          if (data.code == 7) {
            textExpired = `<p class='warning-plan'> Su plan Seleccionado ha expirado, activa otro plan</p>`;
            finalText = text1 + textExpired + buttonReload;
         }              

         if (data.code == 8) {
            textExpired = `<p class='warning-plan' style="font-size:12px;">
             Su plan Seleccionado ha superado el limite de consultas</p>`;
            finalText = text1 + textExpired + buttonReload;
          }
        if (data.code == 9) {
            textExpired = `<p class='warning-plan' style="font-size:12px;">
             Su plan Seleccionado ha superado el limite de consultas, seleccione otro</p>`;
            finalText = text1 + textExpired + buttonChangePlan;
          } 
        if (data.code == 10) {
            textExpired = `<p class='warning-plan' style="font-size:12px;">
                            Su plan Seleccionado ha superado el limite de consultas, activa otro plan</p>`;
            finalText = text1 + textExpired + buttonReload;
         }                               
          $("#chosen-plan").html(finalText);
      }
      else{
          selectPlanBtn = `<center><button id="change_plan" type="button" class="btn btn-xs btn-ligth-blue cap"
                            data-toggle="modal" data-target="#changePlan">${TRANS_CHANGE_PLAN}
                            </button>`;

              if (data.code == 3) {
                  $("#chosen-plan").html(`<center><button id="change_plan" type="button" class="btn btn-xs btn-ligth-blue cap"
                                        data-toggle="modal" data-target="#changePlan">${TRANS_SELECT_PLAN}
                                        </button>`);
              }
              if(data.code == 2) {
                 $("#chosen-plan").html(`<div> No tienes un plan de consumo activo </div>`);       
                 $("#chosen-plan").addClass("no-activeplan");
              }
                if (data.code == 1) {
                    $("#chosen-plan").html(
                    "<center> <button type='button' class='btn btn-md btn-ligth-blue cap' data-toggle='modal'"+
                    "data-target='#reload'>"+ TRANS_RELOAD +"</button> </center>");
                }
          }
    });
});  
   $("#chosen-plan").toggleClass('hidden');
// });

});
