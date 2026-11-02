const mainNav = document.querySelector("#main-navigation");

if (mainNav) {
  mainNav.addEventListener("click", (event) => {
    const navigationLink = event.target.closest("a");

    if (navigationLink && window.innerWidth < 992) {
      bootstrap.Collapse.getOrCreateInstance(mainNav).hide();
    }
  });
}
