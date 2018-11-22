
$(function() {
    const HTTP_CODES = {OK:200, CREATED:201, BAD_REQUEST:400, NOT_FOUND:404}

    $(document).ready(function() {
    });

    $('.associate').click(function(event) {
        var associate_id = $(this).prop('id').slice(10);
        var url = associate_detail_url.replace('0', associate_id);
        window.location.replace(url);
    });
});
