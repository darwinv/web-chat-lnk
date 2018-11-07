$(document).ready(function () {

function getMobileOperatingSystem() {
    var userAgent = navigator.userAgent || navigator.vendor || window.opera;

        // Windows Phone must come first because its UA also contains "Android"
      if (/windows phone/i.test(userAgent)) {
          console.log("Windows Phone");
      }

      if (/android/i.test(userAgent)) {
          if (confirm("¿Deseas usar la app?")) {
          console.log("android");
          var url_link = "https://play.google.com/store/apps/details?id=pe.com.linkup.android.user&hl=es";
          var play_store = "https://play.app.goo.gl/?link="+url_link;
          window.location.href = play_store;
          }
      }

      // iOS detection from: http://stackoverflow.com/a/9039885/177710
      if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
          var url_link = "https://testflight.apple.com/join/YwSCtt0f";
          window.location.href = url_link;
      }

      console.log(userAgent);
  }
  getMobileOperatingSystem();

});
