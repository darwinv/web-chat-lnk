$(document).ready(function () {


$(document).on('submit','#create-match',function(event){
        event.preventDefault();
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
          data["file"] = arr;
        }

        sendAjaxService(data, function(response) {
            if (response.status_code == "200") {
              console.log("exitoso");
            }else {
              console.log("error: " +response.status_code);
              console.log(response);
            }

        }, type="POST")
    });
}); // Cierra document Ready
