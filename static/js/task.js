$(document).ready(function () {
    var completeTask = function () {
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        var dataID = $(this).closest('div.card').data('id');
        $.ajax({
            url: '/tasks/' + dataID + '/complete/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataID
            },
            type: 'post'
        });
    }

    var deleteTask = function () {
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        var dataID = $(this).closest('div.card').data('id');
        $.ajax({
            url: '/tasks/' + dataID + '/delete/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataID
            },
            type: 'post',
            success: function () {
                $('#taskCard[data-id="' + dataID + '"]').remove();
            }
        });
    }

    // update task
    $("#largeModal").on('click', '.task-complete', completeTask);
    $("#largeModal").on('click', '.task-delete', deleteTask);
});