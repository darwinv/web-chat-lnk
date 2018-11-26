$(document).ready(function () {


$(document).on('submit','#create-match',function(event){
        event.preventDefault();
        $("#cont-create-match #animacion1").toggleClass("hidden");
        var fileToUpload = $('#file_match').prop('files');
        console.log(fileToUpload)
        var speciality = $('select[name=category]').val();
        var subject = $('#subject').val();
        var data = {
          "category": speciality,
          "subject": subject,
          "url": `client/matchs/`,
        }

        if (fileToUpload != undefined){
          // var fileObj = {
          //   "file_url": fileToUpload.name,
          //   "content_type": 2
          // };
          var arr = []
          for (var i = 0; i < fileToUpload.length; i++) {
              // console.log(files[i].name);
              arr.push({"file_url":fileToUpload[i].name, "content_type":2});
          }
          for (const file in fileToUpload) {
             console.log(fileToUpload[file].name);
          }
          // arr.push(fileObj);
          data["file"] = JSON.stringify(arr);
        }
        // console.log(data);
        $("#submit-match").attr("disabled", true);

        sendAjaxService(data, function(response) {
            if (response.status_code == "201") {
              setTimeout(function(){
                console.log("exitoso");
              }, 2000);
              console.log(response);
              var files_data = $('#file_match').prop('files');

                if (files_data.length > 0){
                  console.log('entro')
                  upload_files_ids(response.files_id, files_data, response.id);
                }
                else{
                  $("#cont-create-match #animacion1").toggleClass("hidden");
                  $('#cont-create-match #message').addClass('successful');
                  $('#cont-create-match #message').text("Se ha Solicitado correctamente");
                  window.location.href = url_matchs_client;
                }
            }
            else {
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

    function upload_files_ids(arr_ids, files, id_match) {
      prefixFile = "DOC";
      var date = new Date();
      var datestring = date.yyyymmdd();
      var formData = new FormData();

      // formData.append('file', files);
      $.each(files, function(i, file) {

        extension = (/[.]/.exec(file.name)) ? /[^.]+$/.exec(file.name) : undefined;
        fileName = `${prefixFile}-${datestring}-${arr_ids[i]}.${extension}`;
        //Agregando file al formulario
        formData.append("file-"+i, file, fileName);
    });

      formData.append('url', 'match/upload_files/'+id_match+'/');
      formData.append('use_method', 'PUT');

      uploadFileAjax(formData, function(response) {
        console.log(response);
        if (response.status_code = "200"){
          $("#cont-create-match #animacion1").toggleClass("hidden");
          $('#cont-create-match #message').addClass('successful');
          $('#cont-create-match #message').text("Se ha Solicitado correctamente");
          window.location.href = url_matchs_client;
        }
        else{
          console.log("response: ", response);
        }


      });
  }


  Date.prototype.yyyymmdd = function() {
    var mm = this.getMonth() + 1; // getMonth() is zero-based
    var dd = this.getDate();

    return [this.getFullYear(),
            (mm>9 ? '' : '0') + mm,
            (dd>9 ? '' : '0') + dd
           ].join('');
  };
}); // Cierra document Ready
