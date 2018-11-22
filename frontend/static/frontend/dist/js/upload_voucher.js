
$(function() {
    const HTTP_CODES = {OK:200, CREATED:201, BAD_REQUEST:400, NOT_FOUND:404}

    $(document).ready(function() {
        $('#send-button').prop('disabled', true);
        var arr_products = []
        
        $('#upload-voucher-modal').on('shown.bs.modal', function (e) {
            if (typeof newPurchase !== "undefined"){
                $("#ommit").toggleClass("hidden");
                $("#ommit-button").prop('disabled', true);
             }
        }); 
    });

    $('#voucher-section').click(function(event) {
        $('#file-input').trigger('click');
    });

    $('#file-input').change(function(event) {
        var file = $('#file-input').prop('files')[0];
        if (file == null || file == "") {
            return;
        }

        var preview = $('#voucher-img')
        var reader  = new FileReader();

        reader.onloadend = function () {
           preview.attr('src', reader.result);
           $('#send-button').prop('disabled', false);
        }

        reader.readAsDataURL(file);
    });

    $('#upload-voucher-form').on('submit', function(event) {
        event.preventDefault();
        if (typeof newPurchase !== "undefined"){
            sendPurchase(false);
        } else{
            $("#upload-animation").toggleClass("hidden");
            $('#send-button').prop('disable', true);
            upload();
        }
    });

    $('#terms').change(function() {
        if($(this).is(":checked")) {
            $('#ommit-button').prop('disabled', false);
        }
        else{
            $('#ommit-button').prop('disabled', true);
        }
    });

    $('#ommit-button').click(function(e){
        omitir = true;
       sendPurchase(omitir);
    });

    function sendPurchase(omitir){
        $('#ommit-button').prop('disabled', true);
        var isFee = $('#total').data('isfee');
        var isFeeSend = isFee == 1 ? true : false;
        var products = [];
        var prods = JSON.parse(idProducts)
        console.log(typeof(prods));
            
        prods.forEach(function(id) {
            products.push({"product_type":1, "is_billable":true,
                            "plan_id":id,"quantity":1
                            });
            });

        data = {
                "place":"BCP",
                "description": "Plan de Consulta",
                "is_fee": isFeeSend,
                "client": userID,
                "url": 'purchase/',
                "products":JSON.stringify(products),
                "serialize":'products'
              }

        sendAjaxService(data, function(response) {
            console.log(data);
            if (response.status_code == "201") {
                if (omitir == true) {
                    setTimeout(function(){
                        $('#upload-voucher-modal').modal('hide');
                        $('#thanks-for-payment-modal').modal('show');  
                    }, 2000);    
                } else {
                    url = `clients/sales/upload_files/${response.id}/`;
                    $("#upload-animation").toggleClass("hidden");
                    upload2(url);
                }
            } else {
               //console.log
                console.log(response)
            }
        },'POST');
    }  

    function upload2(url_upload){
        var formData = new FormData(document.getElementById('upload-voucher-form'));
        formData.append('file', $('#file-input').prop('files')[0]);
        formData.append('url', url_upload);
        formData.append('use_method', 'PUT');


        uploadFileAjax(formData, function(response) {
            $("#upload-animation").toggleClass("hidden");
            $('#send-button').prop('disable', false);
            if (response.status_code === HTTP_CODES.OK) {
                $('#upload-voucher-modal').modal('hide');
                $('#thanks-for-payment-modal').modal('show');
            }
        });
    }

    function upload() {
        var formData = new FormData(document.getElementById('upload-voucher-form'));
        formData.append('file', $('#file-input').prop('files')[0]);
        formData.append('url', upload_url);
        formData.append('use_method', 'PUT');

        uploadFileAjax(formData, function(response) {
            $("#upload-animation").toggleClass("hidden");
            $('#send-button').prop('disable', false);
            if (response.status_code === HTTP_CODES.OK) {
                $('#upload-voucher-modal').modal('hide');
                $('#thanks-for-payment-modal').modal('show');
            }
        });
    }
});
