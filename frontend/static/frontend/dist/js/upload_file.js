$(function() {
  // Plugin de subida de archivos
  $('#file-linkup').fileinput({
      language: 'es',
      showCaption: false,
      showUpload: false,
      showBrowse: false,
      showCancel:false,
      previewClass: "previewClass2",
      uploadUrl: "/none/",
      actionUpload: "",
      autoPlay: false,
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

  $(document).on('click', ".kv-file-content", function(){
   // click videos
   console.log("click");
   $(this).parents(".file-preview-frame").first().find('.kv-file-zoom').first().click();
  });
  //Despliega carga de archivos
  $(".pick-file").click(function(){
    var ele = $(this);
    if (ele[0].id == "img") {
      $('#file-linkup').attr("accept","image/*");
    }else{
      $('#file-linkup').removeAttr("accept");
    }
    $('#file-linkup').click();
    
    //evento se activa luego de cargar la vista previa del archivo
    $('#file-linkup').on('fileloaded', function(event, file, previewId, index, reader) {
        // console.log(previewId + "- fileloaded - " + ele[0].id);
        $("#"+previewId).data("type", ele[0].id);
    })
  });
});
