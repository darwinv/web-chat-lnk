$(function () {
    bank = '#id_bank'
    operation_number = '#id_operation_number'
    payment_type = '#id_payment_type'
    update_bank($(payment_type));
    $(document).on('change', payment_type, function() {
        update_bank($(this));
    });

    function update_bank($this){
        // funcion creada para actualizar banco

        if ($this.val() == 1 || $this.val() ==3) {
            $(bank).prop('required',false);
            $(bank).parent('.form-group').hide();
            $(operation_number).prop('required',false);
            $(operation_number).parent('.form-group').hide();
        }else{
            $(bank).prop('required',true);
            $(bank).parent('.form-group').show();
            $(operation_number).prop('required',true);
            $(operation_number).parent('.form-group').show();
        }

    }

});
