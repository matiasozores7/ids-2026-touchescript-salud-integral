const loginTabs = document.querySelectorAll(".login-tab");
const loginRole = document.querySelector("#login-role");
const loginSubmit = document.querySelector(".login-submit");

loginTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const isPatient = tab.dataset.role === "paciente";
    loginTabs.forEach((item) => {
      const active = item === tab;
      item.classList.toggle("active", active);
      item.setAttribute("aria-selected", String(active));
    });
    loginRole.value = tab.dataset.role;
    loginSubmit.disabled = !isPatient;
  });
});