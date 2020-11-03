$(document).ready(function () {
	var ShowForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr('data-url'),
			type: 'get',
			dataType: 'json',
			beforeSend: function () {
				$("#modal").modal('show');
			},
			success: function (data) {
				$("#modal .modal-content").html(data.html_form);
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
					$("#modal .modal-content").html(data.html_form);
				}
			}
		});
		return false;
	}

	// create
	$("#navbarNavDropdown").on('click', '.show-form-create-navbar', ShowForm);
	$("#homeButtons").on('click', '.show-form-create-homepage', ShowForm);
	$("#modal").on('submit', '.create-form', SaveForm);

	// update
	$("#boardTitle").on('click', '.show-form-update', ShowForm);
	$("#modal").on('submit', '.update-form', SaveForm);
	
	// delete
	$("#boardTitle").on('click', '.show-form-delete', ShowForm);
	$("#applicationButtons").on('click', '.show-form-delete', ShowForm);
	$("#modal").on('submit', '.delete-form', SaveForm);
});
