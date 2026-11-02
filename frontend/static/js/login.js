const loginTabs = document.querySelectorAll(".login-tab");
const loginRole = document.querySelector("#login-role");

loginTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    loginTabs.forEach((item) => {
      const active = item === tab;
      item.classList.toggle("active", active);
      item.setAttribute("aria-selected", String(active));
    });
    loginRole.value = tab.dataset.role;
  });
});