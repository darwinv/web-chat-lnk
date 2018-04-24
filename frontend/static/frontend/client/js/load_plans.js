$(document).ready(function () {

// cargar planes activos para el seleccionable en el modal
  $('#changePlan').on('shown.bs.modal', function (e) {
  // do something...
  url = $('#chosen-plan').data('url');
  $.get( url, function( data ) {
    $.each(data.results, function(i,v){
      // console.log(i);
      var html = "<input name='active_plans' value='"+v.id+"' type='radio'>";
      var text = `<label class='font-size25 marL5 marB-5'> ${v.plan_name} </label> <br>
      <small class='marL20'>${TRANS_QUERIES}: ${v.available_queries} / ${v.query_quantity} </small>
      <br><small class='marL20'>${TRANS_VALIDITY_MONTHS}: ${v.validity_months} </small> <br>`;
      // console.log(v.id);
      $('#change-chosen').prepend(
        "<div class='container-modal-inputs'>"+html+text+'</div>');
    });
    // console.log(data);
  },
  "json" );
});


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
      console.log(data);
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
