$(document).ready(function () {
    $('#list-match-content').data("url",'client/matchs/');  // Url a consumir
    $('#list-match-content').data("page", 1);
    $(".match").each(function(){
        // Renderizamos el time en el listado
        // le damos  formato a de fecha a todas las fechas de match
        var timeMatch = $(this).data("time");
        var status = $(this).data("status");
        var timeMatchFixed = dateTextCustom(moment.utc(timeMatch), "-05:00");
        $(this).find("small.time").text('Solicitado: '+ timeMatchFixed);
        if (status == 1){
            $(this).find("p.status").text("Estado: Esperando Respuesta");
        }
    });


    $('#list-match-content').scroll(function() {
        // Cuando se realiza Scroll sobre el listado
        win = $('#list-match-content');
        if (win.canMakeScrollPagination()){
            
          loadMatchs(win);
        }
      });


    function loadMatchs(win){
        win.sendAjaxPagination(function(data) {
          showMatchs(data.results)
        });
      }

      function showMatchs(dataList){
        // maquetar listado de planes segun objeto iterable
        $.each(dataList, function(i,v){
          var html = "<input name='active_plans' value='"+v.id+"' type='radio'>";
          var text = `<label class='font-size25 marL5 marB-5'> ${v.plan_name} </label> <br>
          <small class='marL20'>${TRANS_QUERIES}: ${v.available_queries} / ${v.query_quantity} </small>
          <br><small class='marL20'>${TRANS_VALIDITY_MONTHS}: ${v.validity_months} </small> <br>`;
          
          $('#change-chosen-list').append("<div class='container-modal-inputs'>"+html+text+"</div>");
        });
      }

    // win.sendAjaxPagination(function(resp){
    //     console.log(resp);
    // });
});