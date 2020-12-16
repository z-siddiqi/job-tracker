$(document).ready(function () {
	var showModal = function () {
		var btn = $(this);
		var modalId = btn.data('modal');
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			success: function (response) {
				if (response.status != 403) {
					$(modalId + " .modal-content").html(response.form);
					$(modalId).modal('show');
				}
			}
		});
		return false;
	}

	var saveModalForm = function () {
		var form = $(this);
		$.ajax({
			url: form.attr('action'),
			data: form.serialize(),
			type: 'post',
			dataType: 'json',
			success: function (response) {
				if (response.url) {
					window.location.href = response.url;
				} else if (response.task) {
					appendTask(response.task);
					form[0].reset();  // remove text from input box
				} else {
					form.closest('.modal-content').html(response.form)
				}
			}
		});
		return false;
	}

	var appendTask = function (task) {
        $("#taskList").append('<div class="card mb-1" id="taskCard" data-id="' + task.id +
            '"><div class="card-body"><div class="form-check-inline mw-85 overflow-hidden">' +
            '<input class="form-check-input float-left task-complete" type="checkbox"><label class="form-check-label">' +
            task.task + '</label></div><button type="button" class="close float-right task-delete">' +
            '<span aria-hidden="true"><i class="bx bxs-x-square"></i></span></button></div></div>');
    }

	// show modal
	$("#container").on('click', '.show-modal', showModal);

	// save form
	$("#smallModal, #largeModal").on('submit', '.form', saveModalForm);	
});