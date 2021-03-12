// modal
function showModal() {
	let btn = this;
	let modalId = btn.dataset.modal;
	let url = btn.dataset.url;
	fetch(url, {
		headers: {
			'Accept': 'application/json',
			'X-Requested-With': 'XMLHttpRequest',
		},
	})
		.then(response => response.json())
		.then(data => {
			if (data.status != 403) {
				let modal = document.getElementById(modalId);
				let modalContent = modal.getElementsByClassName("modal-content")[0];
				modalContent.innerHTML = data.form;
				$(modal).modal('show');  // need to change
			}
		})
		.catch(err => console.log(err))
	return false;
}

function saveModalForm() {
	let form = this;
	let formData = new FormData(form);
	fetch(form.action, {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'X-Requested-With': 'XMLHttpRequest',
		},
		body: formData,
	})
		.then(response => response.json())
		.then(data => {
			if (data.form) {
				// form invalid
				let modalContent = form.closest('.modal-content');
				modalContent.innerHTML = data.form;
			} else if (data.status == 302) {
				// form valid with redirect
				window.location.href = data.url;
			} else if (data.status == 200) {
				// form valid without redirect
				if (data.task) {
					// add task
					appendTask(data.task);
					form.reset();
				} else if (data.board) {
					// edit board title
					let modal = form.closest('.modal');
					let boardTitle = document.getElementById("boardTitle").getElementsByTagName("h3")[0];
					boardTitle.innerText = data.board.title;
					$(modal).modal('toggle');  // need to change
				} else {
					// reload jobs
					loadJobs();
					let modal = form.closest('.modal');
					$(modal).modal('toggle');  // need to change
				}
			}
		})
		.catch(err => console.log(err))
	return false;
}

function clearModal() {
	let modalContent = this.getElementsByClassName("modal-content")[0];
	modalContent.innerHTML = "";
}

// job
function loadJobs() {
	let url = window.location.pathname + "jobs";
	fetch(url, {
		headers: {
			'Accept': 'application/json',
			'X-Requested-With': 'XMLHttpRequest',
		},
	})
		.then(response => response.json())
		.then(data => {
			let columns = document.getElementsByClassName("jobs-container");
			for (let column of columns) {
				column.innerHTML = "";
			}
			data.forEach(job => {
				let parentColumn = document.getElementById(job.progress);
				appendJob(parentColumn, job);
			})
		})
		.catch(err => console.log(err))
	return false;
}

function scrapeJob() {
	let url = new URL(this.dataset.url, window.location.href);
	let inputUrl = document.getElementById("inputUrl").value;
	url.searchParams.append("jobUrl", inputUrl);
	fetch(url, {
		headers: {
			'Accept': 'application/json',
			'X-Requested-With': 'XMLHttpRequest',
		},
	})
		.then(response => response.json())
		.then(data => {
			document.getElementById("id_company").value = data.company;
			document.getElementById("id_title").value = data.title;
			document.getElementById("id_description").summernote('code', data.description);  // summernote editor init is broken atm
		})
		.catch(err => console.log(err))
}

function appendJob(element, job) {
	const markup = `
			<div class="card btm-shadow mb-2 show-modal" data-modal="largeModal" data-url="/boards/${job.board_slug}/jobs/${job.slug}/edit">
				<div class="card-body p-3 rounded cursor-pointer grey-hover">
					<div class="row no-gutters">
						<div class="col-11">
							<h5 class="mr-3">${job.company}</h5>
						</div>
						<div class="col-1">
							<a href="#" class="float-right show-modal" data-modal="smallModal" data-url="/boards/${job.board_slug}/jobs/${job.slug}/delete">
								<i class="bx bx-trash" id="icon"></i>
							</a>
						</div>
					</div>
					<h5 class="font-weight-bold">${job.title}</h5>
					<p class="text-muted mb-0">${job.deadline}</p>
				</div>
			</div>
		`;
	element.innerHTML += markup;
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