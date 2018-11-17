$(document).ready(function () {

// cargar planes activos para el seleccionable en el modal
  
  $('#change-chosen-list').scroll(function() {
    // Cuando se realiza Scroll sobre el listado
    win = $('#change-chosen-list');
    if (win.canMakeScrollPagination()){
      loadPlansChange(win);
    }
  });
  
  $('#changePlan').on('shown.bs.modal', function (e) {
    // Cuando abre vista modal de los planes
    var win = $('#change-chosen-list'); // Contenedor listado   
    //Inicializando data 
    win.data("url",'clients/plans/');  // Url a consumir
    win.data("page", 0);  // Inicializacion de pagina en 0, solo Modales
    win.data("lastScrollTop", -1) // Inicializamos variable Top solo Modales
    loadPlansChange(win);
  });

  function loadPlansChange(win){
    win.sendAjaxPagination(function(data) {
      showPlansChange(data.results)
    });
  }

  function showPlansChange(dataList){
    // maquetar listado de planes segun objeto iterable
    $.each(dataList, function(i,v){
      var html = "<input name='active_plans' value='"+v.id+"' type='radio'>";
      var text = `<label class='font-size25 marL5 marB-5'> ${v.plan_name} </label> <br>
      <small class='marL20'>${TRANS_QUERIES}: ${v.available_queries} / ${v.query_quantity} </small>
      <br><small class='marL20'>${TRANS_VALIDITY_MONTHS}: ${v.validity_months} </small> <br>`;
      
      $('#change-chosen-list').append("<div class='container-modal-inputs'>"+html+text+'</div>');
    });
  }


  $('#changePlan').on('hidden.bs.modal', function () {
    $(".container-modal-inputs").empty();
    $("#message").empty();
    $("#message").removeClass();
      // do something…
  });

  //Mostrar el input del codigo pin para activar el plan
  $("#activate_pin").click(function(){
    if($("#pincode").hasClass("hidden")){
      $("#pincode").removeClass("hidden");
    }
  });

  //
  $('#getPlansByPin').click(function (e) {
    var code = $("#pinCode").val()
    var url_code = url_get_plans_with_code.replace('0', code);
    $.get( url_code, function( data ) { 
      var plan_detail = `<div class='col-xs-6 col-xs-offset-3 font-sizeLarge'>
      <small> ${data.plan_name} </small> <br>
      <small >${TRANS_QUERIES}: ${data.available_queries} / ${data.query_quantity} </small>
      <br><small>${TRANS_VALIDITY_MONTHS}: ${data.validity_months} </small> `;
      var btnActivar = `<button type="submit"
       class="btn btn-ligth-blue marT10">${TRANS_ACTIVATE}</button></div> `;
      $('#activate_plan').append(plan_detail+btnActivar);
    });
  });

}); // Cierra document Ready
