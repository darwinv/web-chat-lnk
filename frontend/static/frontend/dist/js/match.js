$(document).ready(function () {
 

    function matchsChange(){
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
    }


    $('#list-match-content').data("url",'client/matchs/');  // Url a consumir
    $('#list-match-content').data("page", 1);

    $('#list-match-content').scroll(function() {
        // Cuando se realiza Scroll sobre el listado
        win = $('#list-match-content');
        if (win.canMakeScrollPagination()){
          loadMatchs(win);
        }
      });


    function loadMatchs(win){
        win.sendAjaxPagination(function(data) {
          console.log(data.results);
          showMatchs(data.results);
          matchsChange();
        });
      }

      function showMatchs(dataList){
        // maquetar listado de planes segun objeto iterable
        $.each(dataList, function(i,v){
          var container = `<div class='match list-group-item' data-time='${v.date}' data-status='${v.status}'>
                           <img src='${v.category_image}' alt="imagen-especialidad">
                              <p style="float: right;">
                              <small class="time"> </small>
                              </p>
                              Especialidad: ${v.category}
                              <p class="status"> </p>
                              <a href="#">Ver Detalle</a>   
                            </div>`;
          
          $('#list-match-content').append(container);
        });
      }
      //llamo a matchsChange para arreglar todo
      matchsChange();
});