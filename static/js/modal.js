$(document).ready(function () {
	var showModal = function () {
		var btn = $(this);
		var modalId = btn.data('modal');
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			success: function (response) {
				$(modalId + " .modal-content").html(response.html);
				$(modalId).modal('show');
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
				if (response.form_is_valid) {
					window.location.href = response.redirect_url;
				} else {
					form.closest('.modal').html(response.html)
				}
			}
		});
		return false;
	}

	var clearModal = function () {
		$(this).find('.modal-content').empty();
	}

	// show modal
	$("#container").on('click', '.show-modal', showModal);

	// save form
	$("#smallModal, #largeModal").on('submit', '.form', saveModalForm);

	// clear modal
	$("#smallModal").on('hidden.bs.modal', clearModal);
});