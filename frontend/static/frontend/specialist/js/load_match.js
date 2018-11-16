$(document).ready(function () {

    $('#view_match_modal').on('shown.bs.modal', function (e) {
        // Cuando abre vista modal
        var matchId = $(e.relatedTarget).data('id');
        // var categoryImg = `<center> <img src="{{ match.category_image }}" alt="imagen-especialidad"> </center>`;
        var categoryImg = $("#match_"+matchId).find('img').clone();
        var subject = $("#match_"+matchId).find('p.subject_match').text()
        var attachments = $("#match_"+matchId).find('.files').html()
        categoryImg.appendTo($(e.currentTarget).find('.speciality-img'));
        $(e.currentTarget).find('.subject').html('<h4> Asunto </h4>'+ subject);
        $(e.currentTarget).find('.files_match').html(attachments);


      });


    $('#view_match_modal').on('hidden.bs.modal', function () {
        $(".container-modal-match .subject").empty();
        $(".container-modal-match .speciality-img").empty();
        $(".container-modal-match .files_match").empty();
        // $("#message").empty();
        // $("#message").removeClass();
            // do something…
    });

    $('#decline_match_modal').on('shown.bs.modal', function (e) {
        $('#view_match_modal').modal('hide');

    }); 

});