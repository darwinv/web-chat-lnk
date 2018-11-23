$(function() {
    var regular = `<div class="clasification-plan">
                        <span>Planes Regulares</span>
                       Emprendedores, Microempresarios y Profesionales Independientes.
                    </div>`;
    var corporative = `<div class="clasification-plan">
                        <span>Planes Corporativos</span>
                        Emporios Comerciales, Pequeñas y Medianas Empresas.
                    </div>`;
    var clasification = 0;
    $(".plan-cell").each(function(){
        clasification_plan = $(this).data("clasification");
        if (clasification != clasification_plan) {
            if (clasification_plan == 1) {
                html = regular
            }else if (clasification_plan == 2) {
                html = corporative
            }else{
                html = ""
            }            
            $(this).before(html);
            clasification = clasification_plan;
        }
    });
    var isFee = 0;
    $("#back").click(function(){
        $("#plan-list").toggleClass("hidden");
        $("#modality-payment").toggleClass("hidden");
        
    });

    $("#next").attr("disabled",true);

    $("#next").click(function(){
        console.log(isFee);
        sessionStorage.clear();
        $("#plan-list").toggleClass("hidden");
        $("#modality-payment").toggleClass("hidden");
        $("#contado").html('');
        $("#credito").html('');
        var acum = 0;
        var acumIsFee = 0;
        var plansSelected = $('.checkbox-plan:checkbox:checked');
        

            $.each(plansSelected, function(i, val) {

                    var queryQuantity = $(val).data("quantity");
                    var namePlan = $(val).data("name");
                    var monthValidity = $(val).data("validity");
                    var pricePlan = $(val).data("price");
                    var queryByFees = queryQuantity / monthValidity;
                    var priceByFee = pricePlan / monthValidity;

                    var htmlPlan = `<div>
                                        <div class="plan-title">${namePlan} </div>
                                        <div class="white"> 
                                            ${queryQuantity} consulta (s)</br>
                                            Vigencia ${monthValidity} mes (es)</br>
                                         <div class="plan-price">S./ ${pricePlan} </div>
                                        </div>
                                    </div>`;

                    var Fees = `<span class="white"> Cuotas:${monthValidity} - Consultas por cuota: ${queryByFees} 
                                - Cuota del mes: S./ ${priceByFee}</span>`;      

                    $("#contado").append(htmlPlan+'<hr>');
                    $("#credito").append(htmlPlan+Fees+'<hr>');
                    acumIsFee = acumIsFee + parseFloat(priceByFee);
                    acum = acum + parseFloat(pricePlan);
     
                var acumFormat = parseFloat(Math.round(acum * 100) / 100).toFixed(2);
               $("#total").text(`S./ ${acumFormat}`);                    
            });
            var acumIsFeeFormat = parseFloat(Math.round(acumIsFee * 100) / 100).toFixed(2);
            var acumFormat1 = parseFloat(Math.round(acum * 100) / 100).toFixed(2);
            sessionStorage.setItem('totalIsFee', acumIsFeeFormat);
            sessionStorage.setItem('total', acumFormat1);       
      });

    $(".nav-tabs a").click(function(){
        $(this).tab('show');
    });
  
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        isFee = parseInt($(e.target).data("isfee")); // activated tab
        console.log(isFee);
        if (isFee == 1) {
            acumIsFeeFormat = sessionStorage.getItem("totalIsFee");
            $("#total").text(`S./ ${acumIsFeeFormat}`);     
        }else{
            acumIsFeeFormat1 = sessionStorage.getItem("total");
            $("#total").text(`S./ ${acumIsFeeFormat1}`);     
        }
      });


    $("#summary-button").click(function(){
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            console.log(isFee);
            var total;
            if(isFee==0){
               total = sessionStorage.getItem("total");
            }
            else{
                total = sessionStorage.getItem("totalIsFee"); 
            }
            $("#plan-list").append(`<form id="send_summary" action="${url_summary_plans}" method="POST"> 
                                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                                    <input type="hidden" name="modality" value="${isFee}">
                                    <input type="hidden" name="total" value="${total}">`);
            var checkBoxPlans = $('.checkbox-plan:checkbox:checked');

            $.each(checkBoxPlans, function(i, val) {
                $("#send_summary").append(val);
            });
        $("#send_summary").append(`</form>`);
        $("#send_summary").submit();
    });


    $(".checkbox-plan").change(function(){
        var checkBoxPlans = $('.checkbox-plan:checkbox:checked');
        if (checkBoxPlans.length < 1){
          $("#next").attr("disabled",true);
         }
        else{
         $("#next").removeAttr("disabled");
        } 
    });

});