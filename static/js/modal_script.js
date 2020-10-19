$(document).ready(function () {
	var ShowForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType: 'json',
			beforeSend: function () {
				$('#modal-app').modal('show');
			},
			success: function (data) {
				$('#modal-app .modal-content').html(data.html_form);
			}
		});
	}

	var SaveForm = function () {
		var form = $(this);
		$.ajax({
			url: form.attr('data-url'),
			data: form.serialize(),
			type: form.attr('method'),
			dataType: 'json',
			success: function (data) {
				if (data.form_is_valid) {
					window.location.href = data.redirect_url;
				} else {
					$('#modal-app .modal-content').html(data.html_form);
				}
			}
		});
		return false;
	}

	// board
	$('#board-nav').on('click', '.show-form-delete', ShowForm);
	$('#modal-app').on('submit', '.delete-form', SaveForm);

	// application
	$('#application-buttons').on('click', '.show-form-delete', ShowForm);
	$('#modal-app').on('submit', '.delete-form', SaveForm);
});
