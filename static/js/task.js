$(document).ready(function() {
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $("#createButton").click(function() {
        var form = $("#createTaskForm");
        $.ajax({
            url: form.data('url'),
            data: form.serialize(),
            type: 'post',
            success: function(response) {
                $("#taskList").append('<div class="card mb-1" id="taskCard" data-id="' + response.task.id + 
                '"><div class="card-body"><div class="form-check-inline overflow"><input class="form-check-input float-left"' + 
                'type="checkbox"><label class="form-check-label">' + response.task.title + 
                '</label></div><button type="button" class="close float-right">' + 
                '<span aria-hidden="true"><i class="fas fa-times-circle fa-sm"></i></span></button></div></div>');
            }
        });

        form[0].reset();
    });

    $("#task").keypress(function(event) {
        if (event.key === "Enter") {
            $("#createButton").click();
        }
    });

    $("#taskList").on('click', 'input.form-check-input', function() {
        var dataID = $(this).closest('div.card').data('id');
        $.ajax({
            url: '/tasks/' + dataID + '/complete/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataID
            },
            type: 'post'
        });
    }).on('click', 'button.close', function(event) {
        event.stopPropagation();
        var dataID = $(this).closest('div.card').data('id');
        $.ajax({
            url: '/tasks/' + dataID + '/delete/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataID
            },
            type: 'post',
            success: function() {
                $('#taskCard[data-id="' + dataID + '"]').remove();
            }
        });
    });
});