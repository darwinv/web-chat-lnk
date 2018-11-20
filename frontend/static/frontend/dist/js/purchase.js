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


    $("#next").click(function(){
        $("#plan-list").toggleClass("hidden");
    });

    $(".nav-tabs a").click(function(){
        $(this).tab('show');
    });
});