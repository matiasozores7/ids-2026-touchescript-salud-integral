(() => {
  const specialtySearch = document.querySelector("#admin-specialty-search");
  const specialtyRows = document.querySelectorAll("#specialties-table-body tr");
  const visibleCount = document.querySelector("#specialties-visible-count");
  const emptyState = document.querySelector("#specialties-table-empty");
  const specialtyModal = document.querySelector("#specialty-modal");
  const specialtyForm = specialtyModal?.querySelector("form");
  const modalTitle = document.querySelector("#specialty-modal-title");
  const modalName = document.querySelector("#specialty-name");
  const modalDescription = document.querySelector("#specialty-description");
  const deleteModal = document.querySelector("#specialty-delete-modal");
  const deleteModalName = document.querySelector("#specialty-delete-name");
  const deleteModalConfirm = document.querySelector(
    "[data-specialty-delete-confirm]"
  );
  let specialtyFormToDelete = null;

  const toggleModal = (isOpen) => {
    if (!specialtyModal) return;

    specialtyModal.hidden = !isOpen;
    document.body.classList.toggle("modal-open", isOpen);
    if (isOpen) modalName?.focus();
  };

  const toggleDeleteModal = (isOpen) => {
    if (!deleteModal) return;

    deleteModal.hidden = !isOpen;
    document.body.classList.toggle("modal-open", isOpen);
    if (isOpen) deleteModalConfirm?.focus();
  };

  const closeDeleteModal = () => {
    toggleDeleteModal(false);
    specialtyFormToDelete = null;
  };

  document.querySelector("[data-specialty-modal-open]")?.addEventListener("click", () => {
    specialtyForm?.reset();
    if (specialtyForm) {
      specialtyForm.action = specialtyForm.dataset.specialtyCreateAction;
    }
    if (modalTitle) modalTitle.textContent = "Nueva especialidad";
    toggleModal(true);
  });

  document.querySelectorAll("[data-specialty-edit]").forEach((button) => {
    button.addEventListener("click", () => {
      if (!specialtyForm || !modalName || !modalDescription) return;

      specialtyForm.reset();
      specialtyForm.action = button.dataset.specialtyAction;
      modalName.value = button.dataset.specialtyName;
      modalDescription.value = button.dataset.specialtyDescription;
      if (modalTitle) modalTitle.textContent = "Editar especialidad";
      toggleModal(true);
    });
  });

  document.querySelectorAll("[data-specialty-modal-close]").forEach((button) => {
    button.addEventListener("click", () => toggleModal(false));
  });

  specialtyModal?.addEventListener("click", (event) => {
    if (event.target === specialtyModal) toggleModal(false);
  });

  document.querySelectorAll("[data-specialty-delete-modal-close]").forEach((button) => {
    button.addEventListener("click", closeDeleteModal);
  });

  deleteModal?.addEventListener("click", (event) => {
    if (event.target === deleteModal) closeDeleteModal();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      if (specialtyModal && !specialtyModal.hidden) toggleModal(false);
      if (deleteModal && !deleteModal.hidden) closeDeleteModal();
    }
  });

  specialtySearch?.addEventListener("input", () => {
    const query = specialtySearch.value.trim().toLowerCase();
    let matches = 0;

    specialtyRows.forEach((row) => {
      const isMatch = (row.dataset.specialty ?? "").includes(query);
      row.hidden = !isMatch;
      matches += isMatch ? 1 : 0;
    });

    if (visibleCount) visibleCount.textContent = matches;
    if (emptyState) emptyState.hidden = matches > 0;
  });

  document.querySelectorAll("[data-specialty-delete-form]").forEach((form) => {
    const deleteButton = form.querySelector("[data-specialty-delete-open]");

    deleteButton?.addEventListener("click", () => {
      specialtyFormToDelete = form;
      if (deleteModalName) {
        deleteModalName.textContent = deleteButton.dataset.specialtyName ?? "";
      }
      toggleDeleteModal(true);
    });
  });

  deleteModalConfirm?.addEventListener("click", () => {
    const formToDelete = specialtyFormToDelete;
    closeDeleteModal();
    formToDelete?.requestSubmit();
  });
})();
