$(document).ready(function () {
	var showSmallModal = function () {
		var btn = $(this);
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			success: function (response) {
				$("#smallModal").modal('show');
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
			success: function (response) {
				$("#largeModal").modal('show');
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
		var btn = $(this);
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			success: function (response) {
				$('a.active').each(function () {
					$(this).removeClass('active');
				});
				btn.addClass('active');
				$("textarea.summernoteinplacewidget").summernote('destroy');
				$("#largeModal .modal-body").html(response.html);
			}
		});
		return false;
	}

	var clearModal = function () {
		$(this).find('.modal-content').empty();
		return false;
	}

	// show modal
	$("#container").on('click', '.show-large-modal', showLargeModal);
	$("#container").on('click', '.show-small-modal', showSmallModal);

	// save form
	$("#smallModal, #largeModal").on('submit', '.form', saveModalForm);

	// load job info
	$("#largeModal").on('click', '.load-job-info', loadJobInfo);

	// clear modal
	$("#smallModal, #largeModal").on('hidden.bs.modal', clearModal);
});