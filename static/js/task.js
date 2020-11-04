$(document).ready(function(){
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $("#createButton").click(function() {
        var serializedData = $("#createTaskForm").serialize();

        $.ajax({
            url: $("#createTaskForm").data('url'),
            data: serializedData,
            type: 'post',
            success: function(response) {
                $("#taskList").append('<div class="card mb-1" id="taskCard" data-id="' + 
                response.task.id + '"><div class="card-body">' + response.task.title + 
                '<button type="button" class="close float-right" data-id="' + response.task.id + 
                '"><span aria-hidden="true">&times;</span></button></div></div>');
            }
        });

        $("#createTaskForm")[0].reset();
    });

    $("#taskList").on('click', '.card', function() {
        var dataID = $(this).data('id');
        
        $.ajax({
            url: '/tasks/' + dataID + '/complete/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataID
            },
            type: 'post',
            success: function() {
                var cardItem = $('#taskCard[data-id="' + dataID + '"]');
                cardItem.css('text-decoration', 'line-through').hide().slideDown();
                $("#taskList").append(cardItem);
            }
        });
    }).on('click', 'button.close', function(event) {
        event.stopPropagation();

        var dataID = $(this).data('id');

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