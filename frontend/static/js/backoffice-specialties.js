const specialtySearch = document.querySelector("#admin-specialty-search");
const specialtyRows = document.querySelectorAll("#specialties-table-body tr");
const visibleCount = document.querySelector("#specialties-visible-count");
const emptyState = document.querySelector("#specialties-table-empty");
const specialtyModal = document.querySelector("#specialty-modal");
const modalName = document.querySelector("#specialty-name");

const toggleModal = (isOpen) => {
    specialtyModal.hidden = !isOpen;
    document.body.classList.toggle("modal-open", isOpen);
    if (isOpen) modalName?.focus();
};

document.querySelector("[data-specialty-modal-open]")?.addEventListener("click", () => toggleModal(true));

document.querySelectorAll("[data-specialty-modal-close]").forEach((button) => {
    button.addEventListener("click", () => toggleModal(false));
});

specialtyModal?.addEventListener("click", (event) => {
    if (event.target === specialtyModal) toggleModal(false);
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && specialtyModal && !specialtyModal.hidden) toggleModal(false);
});

specialtySearch?.addEventListener("input", (event) => {
    const query = event.target.value.trim().toLowerCase();
    let matches = 0;

    specialtyRows.forEach((row) => {
        const isMatch = row.dataset.specialty.includes(query);
        row.hidden = !isMatch;
        matches += isMatch ? 1 : 0;
    });

    visibleCount.textContent = matches;
    emptyState.hidden = matches > 0;
});