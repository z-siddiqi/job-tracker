const fetchModalContent = async function (url) {
  const requestOptions = {
    method: "GET",
    headers: { "X-Requested-With": "XMLHttpRequest" },
  };
  const response = await fetch(url, requestOptions);
  const data = await response.json();
  return data.form;
};

const submitForm = async function (form) {
  const url = form.action;
  const formData = new FormData(form);
  const requestOptions = {
    method: "POST",
    headers: { "X-Requested-With": "XMLHttpRequest" },
    body: formData,
  };
  const response = await fetch(url, requestOptions);
  const data = await response.json();
  return data;
};

const setInnerHTML = function (elm, html) {
  elm.innerHTML = html;
  Array.from(elm.querySelectorAll("script")).forEach((oldScript) => {
    const newScript = document.createElement("script");
    Array.from(oldScript.attributes).forEach((attr) =>
      newScript.setAttribute(attr.name, attr.value)
    );
    newScript.appendChild(document.createTextNode(oldScript.innerHTML));
    oldScript.parentNode.replaceChild(newScript, oldScript);
  });
};

const initSummernote = function () {
  const origin = document.querySelector("textarea.summernoteinplacewidget");
  const settings = JSON.parse(
    document.querySelector("#summernoteSettings").textContent
  );
  const additionalSettings = {
    callbacks: {
      // remove formatting on paste
      onPaste: function (e) {
        e.preventDefault();
        const bufferText = (
          (e.originalEvent || e).clipboardData || window.clipboardData
        ).getData("Text");
        setTimeout(function () {
          document.execCommand("insertText", false, bufferText);
        }, 10);
      },
    },
  };
  $(origin).summernote({ ...settings, ...additionalSettings });
};

const showModal = async function (e) {
  e.preventDefault();
  e.stopPropagation();
  const modalId = e.currentTarget.dataset.modal;
  const url = e.currentTarget.href ?? e.currentTarget.dataset.url;
  fetchModalContent(url)
    .then((content) => {
      const modalEl = document.querySelector(modalId);
      const modalContent = modalEl.querySelector(".modal-content");
      setInnerHTML(modalContent, content);
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      modal.show();
    })
    .catch((error) => console.log(error));
};

const renderJobs = function () {
  const templates = { applied: [], phone: [], onsite: [], offer: [] };

  for (job of state.jobs) {
    templates[job.progress].push(jobTemplate(job));
  }

  for (const [progress, templatesArray] of Object.entries(templates)) {
    document.querySelector(`#${progress}`).innerHTML = templatesArray.join("");
  }
};

const jobTemplate = function (job) {
  return `
			  <div class="card btm-shadow cursor-pointer grey-hover mb-2" data-slug="${job.slug}" data-modal="#largeModal" data-url="/boards/${job.board_slug}/jobs/${job.slug}/edit" onclick="showModal(event)">
				  <div class="card-body p-3 rounded">
					  <div class="row g-0">
						  <div class="col-11">
							  <h5 class="me-3">${job.company}</h5>
						  </div>
						  <div class="col-1">
							  <a href="/boards/${job.board_slug}/jobs/${job.slug}/delete" class="float-end" data-modal="#smallModal" onclick="showModal(event)">
				          <i class="bi bi-trash fs-5"></i>
							  </a>
						  </div>
					  </div>
					  <h5 class="fw-bold">${job.title}</h5>
					  <p class="text-muted mb-0">${job.deadline}</p>
				  </div>
			  </div>
		  `;
};
