$(function() {
  // Plugin de subida de archivos
  $('#file-linkup').fileinput({
      language: 'es',
      showCaption: false,
      showUpload: false,
      showBrowse: false,
      showCancel:false,
      uploadUrl: $('#form-chat').data('upload'),
      previewClass: "previewClass2",
      actionUpload: "",
  });

  $('#file-linkup').on('fileclear', function(event) {
    $("#upload-div").addClass('hidden');
  });

  $('#file-linkup').change(function(){
    if($("#upload-div").hasClass('hidden')){
      $("#upload-div").removeClass('hidden');
    }
  });

  $('#file-linkup').on('filereset', function(event) {
    console.log("filereset");
  });
  $('#file-linkup').on('fileremoved', function(event, id, index) {
    console.log('id = ' + id + ', index = ' + index);
  });

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  //Despliega carga de archivos
  $(".pick-file").click(function(){
        $('#file-linkup').click()
        var ele = $(this);
        //evento se activa luego de cargar la vista previa del archivo
        $('#file-linkup').on('fileloaded', function(event, file, previewId, index, reader) {
            //console.log("fileloaded" + ele[0].id);
            $("#"+previewId).data("type", ele[0].id);
            console.log(previewId);
        })
    });

});
