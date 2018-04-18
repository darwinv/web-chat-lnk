$(document).ready(function () {
  $('#changePlan').on('shown.bs.modal', function (e) {
  // do something...
  url = $('#change_plan').data('url');
  console.log(url);
  $.get( url, function( data ) {
    $.each(data.results, function(i,v){
      // console.log(i);
      var html = "<input name='active_plans' value='"+v.id+"' type='radio'>";
      var text = `<label class='font-size25 marL5'> ${v.plan_name} </label> <br>
      <small class='marL20'>queries: ${v.available_queries} / ${v.query_quantity} </small>
      <br><smal class='marL20'> validity months: ${v.validity_months} </small> <br>`;

      console.log(v.id);
      $('#change-chosen').prepend("<div class='contcheck'>"+html+text+'</div>');
    });
    console.log(data);
  },
  "json" );
});




});
