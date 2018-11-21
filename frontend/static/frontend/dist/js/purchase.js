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

    $("#back").click(function(){
        $("#plan-list").toggleClass("hidden");
        $("#modality-payment").toggleClass("hidden");
        
    });

    $("#next").attr("disabled",true);

    $("#next").click(function(){
        $("#plan-list").toggleClass("hidden");
        $("#modality-payment").toggleClass("hidden");
        $("#contado").html('');
        $("#credito").html('');
        var acum = 0;
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
               acum = acum + parseFloat(pricePlan);
            //    console.log(acum)
               var acumFormat = parseFloat(Math.round(acum * 100) / 100).toFixed(2);
               $("#total").text(`S./ ${acumFormat}`);                    
            });
        
      });

    $(".nav-tabs a").click(function(){
        $(this).tab('show');
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