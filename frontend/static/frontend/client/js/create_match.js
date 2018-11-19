$(document).ready(function () {


$(document).on('submit','#create-match',function(event){
        event.preventDefault();
        $("#cont-create-match #animacion1").toggleClass("hidden");
        var fileToUpload = $('#file_match').prop('files')[0];
        var speciality = $('select[name=category]').val();
        var subject = $('#subject').val();
        var data = {
          "category": speciality,
          "subject": subject,
          "url": `client/matchs/`,
        }

        if (fileToUpload != undefined){
          var fileObj = {
            "file_url": fileToUpload.name,
            "content_type": 2
          };
          var arr = []
          arr.push(fileObj);
          data["file"] = JSON.stringify(arr);
        }
        console.log(data);
        $("#submit-match").attr("disabled", true);
        
        sendAjaxService(data, function(response) {
            if (response.status_code == "201") {
              $("#cont-create-match #animacion1").toggleClass("hidden");
              $('#cont-create-match #message').addClass('successful');
              $('#cont-create-match #message').text("Se ha Solicitado correctamente");
              setTimeout(function(){
                console.log("exitoso");
              }, 2000);                    
              window.location.href = url_matchs_client;
            }else {
              $("#cont-create-match #animacion1").toggleClass("hidden");
              $("#submit-match").removeAttr("disabled");
              $('#cont-create-match #message').addClass('error');
              console.log("error: " +response.status_code);
              if (response.category){
                $('#cont-create-match #message').text(response.category);
              }
              console.log(response);
            }

        }, type="POST")
    });
}); // Cierra document Ready
