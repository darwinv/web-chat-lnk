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
   if ($(this).find("img").length != 0 || $(this).find("video").length != 0) {
    $(this).parents(".file-preview-frame").first().find('.kv-file-zoom').first().click();
   }
  });

  $(document).on('click', ".audio-recorder", function(){
   // click videos

   if ($(this).hasClass("recording")) {
      stopRecording(this);
      $(this).removeClass("recording");
    
   }else{
      startRecording(this);
      $(this).addClass("recording");
   }
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




var audio_context;
  var recorder;

  function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    console.log('Media stream created.');

    // Uncomment if you want the audio to feedback directly
    //input.connect(audio_context.destination);
    //console.log('Input connected to audio context destination.');
    
    recorder = new Recorder(input);
    console.log('Recorder initialised.');
  }

  function startRecording(button) {
    recorder && recorder.record();
    console.log('Recording...');
  }

  function stopRecording(button) {
    recorder && recorder.stop();
    console.log('Stopped recording.');
    
    // create WAV download link using audio data blob
    createDownloadLink();
    
    recorder.clear();
  }

  function createDownloadLink() {
    recorder && recorder.exportWAV(function (blob) {
        var url = URL.createObjectURL(blob);
        var div = document.createElement('div');
        var au = document.createElement('audio');
        
        au.classList.add("kv-preview-data");
        au.classList.add("file-preview-audio");        
        au.controls = true;
        au.src = url;
        div.appendChild(au);

        // recordingslist.appendChild(li);        
        $(".file-preview-thumbnails").append(div);
        $('#file-linkup').fileinput('addToStack', blob); // where `fileObj` is the file blob object instance
        $("#upload-div").removeClass("hidden");
        $(".file-drop-zone-title").addClass("hidden");

        
    });
  }

  window.onload = function init() {
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
      window.URL = window.URL || window.webkitURL;
      
      audio_context = new AudioContext;
      console.log('Audio context set up.');
      console.log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
      alert('No web audio support in this browser!');
    }
    
    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
      console.log('No live audio input: ' + e);
    });
  };