$(document).ready(function () {
	var showSmallModal = function () {
		var btn = $(this);
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			beforeSend: function () {
				$("#smallModal").modal('show');
			},
			success: function (response) {
				$("#smallModal .modal-content").html(response.html);
			}
		});
		return false;
	}

	var showLargeModal = function () {
		var btn = $(this);
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			beforeSend: function () {
				$("#largeModal").modal('show');
			},
			success: function (response) {
				$("#largeModal .modal-content").html(response.html);
				if ($("a:contains('Info')").length > 0) {
					$("a:contains('Info')").trigger('click');  // initially load job info
				}
			}
		});
		return false;
	}

	var saveModalForm = function () {
		var form = $(this);
		$.ajax({
			url: form.data('url'),
			data: form.serialize(),
			type: 'post',
			dataType: 'json',
			success: function (response) {
				if (response.form_is_valid) {
					if (response.redirect_url) {
						window.location.href = response.redirect_url;
					}
				} else {
					form.closest('.modal').html(response.html)
				}
			}
		});
		return false;
	}

	var loadJobInfo = function () {
		$('a.active').each(function () {
			$(this).removeClass('active');  // remove active class from current button
		});
		var btn = $(this);
		btn.addClass('active');  // add active class to clicked button
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			success: function (response) {
				$("#largeModal .modal-body").html(response.html);
			}
		});
		return false;
	}

	// show modal
	$("#container").on('click', '.show-large-modal', showLargeModal);
	$("#container").on('click', '.show-small-modal', showSmallModal);

	// save form
	$("#smallModal, #largeModal").on('submit', '.form', saveModalForm);

	// load job info
	$("#largeModal").on('click', '.load-job-info', loadJobInfo);
});