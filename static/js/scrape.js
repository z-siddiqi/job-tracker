$(document).ready(function () {
    var scrapeJob = function () {
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        var inputUrl = $("#inputUrl").val();
        $.ajax({
            url: $(this).data('url'),
            data: {
                csrfmiddlewaretoken: csrfToken,
                jobUrl: inputUrl
            },
            type: 'post',
            success: function (response) {
                $("#id_company").val(response.company);
                $("#id_title").val(response.title);
                $("#id_description").summernote('code', response.description);
            }
        });
    }

    // scrape job posting
    $("#largeModal").on('click', '.scrape-button', scrapeJob);
});