$(document).ready(function () {
 
    function matchsChange(){
        $(".match, .match-detail").each(function(){
          // Renderizamos el time en el listado
          // le damos  formato a de fecha a todas las fechas de match
          var timeMatch = $(this).data("time");
          var status = $(this).data("status");
          var matchID = $(this).data("id"); 
          var timeMatchFixed = dateTextCustom(moment.utc(timeMatch), "-05:00");
         if(status !=5){   
            $(this).find("small.time").text('Solicitado: '+ timeMatchFixed);
          }
          if (status == 1 || status == 2){
              if (roleID == ROLES.specialist) {
                if (status == 1) {
                  declineAcceptBtn = `<center> <button id="match_modal" type="button" class="btn btn-xs btn-ligth-blue cap"
                  data-toggle="modal" data-id="${matchID}" data-target="#view_match_modal">Responde el Match</button> 
                   </center>`;
                      $(this).find("p.status").html(declineAcceptBtn);
                      $(this).find("a.link-match").addClass('hidden');    
                 }else{
                  $(this).find("p.status").text("Estado: Pendiente de Revision"); 
                 }     
              }
              else {
                $(this).find("p.status").text("Estado: Esperando Respuesta"); 
              }
           }
          if (status == 3){
            $(this).find("p.status").text("Estado: Declinado");
         }
         if (status == 4){
           
            if (roleID == ROLES.specialist){
              $(this).find("p.status").text("Estado: Pendiente de Pago por el cliente");
            }else{
              $(this).find("p.status").text("Estado: Pendiente de Pago");
            }
       }
          if (status == 6){
             $(this).find("p.status").text("Estado: Pendiente de Revisión");
          }
          if (status == 5){
            $(this).find("p.status").text("Estado: Aceptado");
          }
      });
    }

    $('#list-match-content').data("url",'client/matchs/');  // Url a consumir
    if (roleID == ROLES.specialist){
      $('#list-match-content').data("url",'specialists/matchs/');  // Url a consumir
    }
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