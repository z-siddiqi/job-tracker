$(document).ready(function () {
    var createTask = function () {
        var form = $(this);
        $.ajax({
            url: form.data('url'),
            data: form.serialize(),
            type: 'post',
            dataType: 'json',
            success: function (response) {
                if (response.form_is_valid) {
                    appendTask(response.task);
                    form[0].reset();  // remove text from input box
                } else {
                    form.closest('.modal').html(response.html)
                }
            }
        });
        return false;
    }

    var appendTask = function (task) {
        $("#taskList").append('<div class="card mb-1" id="taskCard" data-id="' + task.id +
            '"><div class="card-body"><div class="form-check-inline overflow">' +
            '<input class="form-check-input float-left task-complete" type="checkbox"><label class="form-check-label">' +
            task.task + '</label></div><button type="button" class="close float-right task-delete">' +
            '<span aria-hidden="true"><i class="bx bxs-x-square"></i></span></button></div></div>');
    }

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

    // create task
    $("#largeModal").on('submit', '.task-form', createTask);

    // update task
    $("#largeModal").on('click', '.task-complete', completeTask);
    $("#largeModal").on('click', '.task-delete', deleteTask);
});