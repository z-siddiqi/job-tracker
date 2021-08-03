// modal
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
			if (response.form) {
				// form invalid
				form.closest('.modal-content').html(response.form);
			} else if (response.status == 302) {
				// form valid with redirect
				window.location.href = response.url;
			} else if (response.status == 200) {
				// form valid without redirect
				if (response.task) {
					// add task
					appendTask(response.task);
					form[0].reset();
				} else if (response.board) {
					// edit board title
					$("#boardTitle h3").text(response.board.title)
					form.closest('.modal').modal('toggle');
				} else {
					// reload jobs
					loadJobs();
					form.closest('.modal').modal('toggle');
				}
			}
		}
	});
	return false;
}

var clearModal = function () {
	$(this).find('.modal-content').empty();
}

// job
var loadJobs = function () {
	var url = $("#boardButtons .board-edit").data('url').replace('edit', 'jobs')
	$.ajax({
		url: url,
		type: 'get',
		dataType: 'json',
		success: function (response) {
			$("#applied, #phone, #onsite, #offer").empty();
			$.each(response, function (index, val) {
				appendJob(val);
			});
		}
	});
	return false;
}

var scrapeJob = function () {
	var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
	var inputUrl = $("#inputUrl").val();
	$.ajax({
		url: $(this).data('url'),
		data: {
			csrfmiddlewaretoken: csrfToken,
			jobUrl: inputUrl
		},
		type: 'post',
		success: function (response) {
			$("#id_company").val(response.company);
			$("#id_title").val(response.title);
			$("#id_description").summernote('code', response.description);
		}
	});
}

var appendJob = function (job) {
	const markup = `
			<div class="card btm-shadow mb-2 show-modal" data-modal="#largeModal" data-url="/boards/${job.board_slug}/jobs/${job.slug}/edit">
				<div class="card-body p-3 rounded cursor-pointer grey-hover">
					<div class="row no-gutters">
						<div class="col-11">
							<h5 class="mr-3">${job.company}</h5>
						</div>
						<div class="col-1">
							<a href="#" class="float-right show-modal" data-modal="#smallModal" data-url="/boards/${job.board_slug}/jobs/${job.slug}/delete">
								<i class="bx bx-trash" id="icon"></i>
							</a>
						</div>
					</div>
					<h5 class="font-weight-bold">${job.title}</h5>
					<p class="text-muted mb-0">${job.deadline}</p>
				</div>
			</div>
		`;
	$("#" + job.progress).append(markup);
}

// task
var appendTask = function (task) {
	const markup = `
			<div class="card mb-1" id="taskCard" data-id="${task.id}">
				<div class="card-body">
					<div class="form-check-inline mw-85 overflow-hidden">
						<input class="form-check-input float-left task-complete" type="checkbox">
						<label class="form-check-label">
							${task.task}
						</label>
					</div>
					<button type="button" class="close float-right task-delete">
						<span aria-hidden="true"><i class="bx bxs-x-square"></i></span>
					</button>
				</div>
			</div>
		`;
	$("#taskList").append(markup);
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