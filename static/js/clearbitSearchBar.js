const fetchClearbitResults = async function (query) {
  const requestOptions = {
    method: "GET",
  };
  const url = `https://autocomplete.clearbit.com/v1/companies/suggest?query=:${query}`;
  const response = await fetch(url, requestOptions);
  const data = await response.json();
  return data;
}

const initClearbitSearchBar = function (inputId, buttonId, menuId) {
  const input = document.getElementById(inputId);
  const button = document.getElementById(buttonId);
  const menu = document.getElementById(menuId);
  button.addEventListener("show.bs.dropdown", async (e) => {
    const wrapper = document.querySelector("#div_id_company");
    menu.style.width = wrapper.offsetWidth + "px";
    const results = await fetchClearbitResults(input.value);
    results.length > 0
      ? renderResults(input, results, menu)
      : renderError(menu);
  });
  button.addEventListener("hidden.bs.dropdown", (e) => {
    menu.innerHTML = "";
  });
}

const renderError = function (container) {
  const li = document.createElement("li");
  const span = document.createElement("span");
  span.classList.add("dropdown-item");
  span.innerText = "No results.";
  li.appendChild(span);
  container.append(li);
}

const renderResults = function (input, results, container) {
  if (results.length > 3) {
    results = results.slice(0, 3);
  }
  results.forEach((result) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.classList.add("d-flex", "justify-content-between", "dropdown-item");
    a.href = "#";
    const span = document.createElement("span");
    span.innerText = result.name;
    a.appendChild(span);
    let img = document.createElement("img");
    img.src = result.logo + "?size=130";
    img.width = "25";
    a.appendChild(img);
    a.addEventListener("click", (e) => {
      e.preventDefault();
      const name = e.currentTarget.querySelector("span").textContent;
      const logo = e.currentTarget.querySelector("img").src;
      input.value = name;
      document.querySelector("#logo").src = logo;
      document.querySelector("#id_logo").value = logo;
    });
    li.appendChild(a);
    container.append(li);
  });
}
