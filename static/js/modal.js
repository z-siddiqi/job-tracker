$(document).ready(function () {
	var showSmallModal = function () {
		var btn = $(this);
		$.ajax({
			url: btn.data('url'),
			type: 'get',
			dataType: 'json',
			success: function (response) {
				$("#smallModal .modal-content").html(response.html);
				$("#smallModal").modal('show');
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
				$("#largeModal .modal-content").html(response.html);
				$("#largeModal").modal('show');
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
					if (response.redirect_url) {
						window.location.href = response.redirect_url;
					} else {
						showSuccessAlert();
					}
				} else {
					form.closest('.modal').html(response.html)
				}
			}
		});
		return false;
	}

	var showSuccessAlert = function () {
        $(".alert-success").prop('hidden', false);
        setTimeout(function () {
            $(".alert-success").prop('hidden', true);
        }, 1000);
    }

	var clearModal = function () {
		$(this).find('.modal-content').empty();
	}

	var reloadPage = function () {
		setTimeout(function () {
			location.reload();
		}, 500);
	}

	// show modal
	$("#container").on('click', '.show-large-modal', showLargeModal);
	$("#container").on('click', '.show-small-modal', showSmallModal);

	// save form
	$("#smallModal, #largeModal").on('submit', '.form', saveModalForm);

	// clear modal
	$("#smallModal").on('hidden.bs.modal', clearModal);
	$("#largeModal").on('hidden.bs.modal', reloadPage);
});