$(function () {
	load_country_restrictions($('#id_residence_country'));
	$(document).on('change', '#id_residence_country', function() {
		load_country_restrictions($(this));
	});

	function load_country_restrictions($this){
		// funcion creada para manejar ubigeo y documento para usuarios extanjeros y locales

		if ($this.val()==1 || $this.val()=="") { //Si pais es peru, muestra fields address
			$('#id_ruc,#id_department,#id_province,#id_district,#id_street').prop('required',true);
			$('#id_department,#id_province,#id_district,#id_street').show();
			$('#id_foreign_address').hide();

		}else{ // Si es extranjero, oculta ubigeo y deja campo de texto
			$('#id_ruc,#id_department,#id_province,#id_district,#id_street').prop('required',false);
			$('#id_department,#id_province,#id_district,#id_street').hide();
			$('#id_foreign_address').show();
		}

	}
});

$(document).ready(function () {
	$("#inputFile").attr('required',true);
    console.log("pase");
});
