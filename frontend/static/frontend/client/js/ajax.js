$(document).ready(function () {

  $("#change-chosen").submit(function(e){
      e.preventDefault();
    plan = $('input[name=active_plans]:checked', '#change-chosen').val();
    url_plan = $("#change-chosen").data("url");
    url_plan = url_plan + '/' + plan;
    $.ajax({
        type:"POST",
        url:url_plan,
        data: {
               'is_chosen': 1
               },
        success: function(){
            $('#message').html("<h2>Contact Form Submitted!</h2>")
        }
   });
  });


});
