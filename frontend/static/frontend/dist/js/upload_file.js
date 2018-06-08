$(function() {
// Plugin de subida de archivos
    $('#file-linkup').fileinput({
        language: 'es',
        showCaption: false,
        showUpload: false,
        showBrowse: true,
        uploadUrl: $('#form-chat').data('upload'),
    });


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

//Despliega carga de archivos
    $(".pick").click(function(){
          $('#file-linkup').click()
           var ele = $(this);
          console.log(ele);
          //$('#file-linkup').trigger('click');
          //evento se activa luego de cargar la vista previa del archivo
          $('#file-linkup').on('fileloaded', function(event, file, previewId, index, reader) {
              console.log(file);
              //console.log("fileloaded" + ele[0].id);
              $("#"+previewId).data("type", ele[0].id);
              console.log(previewId);
          })
      });

$('#file-linkup').change(function(){
    console.log("en change");
  if($("#upload-div").hasClass('hidden')){
      $("#upload-div").removeClass('hidden');
     }
});
});
