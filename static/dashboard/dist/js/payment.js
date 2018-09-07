$(function () {
    bank = '#id_bank'
    id_payment_type = '#id_payment_type'
    update_bank($(id_payment_type));
    $(document).on('change', id_payment_type, function() {
        update_bank($(this));
    });

    function update_bank($this){
        // funcion creada para actualizar banco

        if ($this.val() == 1 || $this.val() ==3) {
            $(bank).prop('required',false);
            $(bank).parent('.form-group').hide();
        }else{
            $(bank).prop('required',true);
            $(bank).parent('.form-group').show();
        }

    }

});
