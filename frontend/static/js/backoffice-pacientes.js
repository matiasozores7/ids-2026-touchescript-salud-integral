(() => {
  const searchInput = document.querySelector("#buscar-paciente");
  const tableRows = document.querySelectorAll("#pacientes-table-body tr");
  const countNum = document.querySelector("#pacientes-count-num");
  const emptyMsg = document.querySelector("#pacientes-table-empty");

  const patientModal = document.querySelector("#patient-modal");
  const patientForm = document.querySelector("#form-paciente");
  const modalTitle = document.querySelector("#patient-modal-title");
  const campoNombre = document.querySelector("#campo-nombre");
  const campoApellido = document.querySelector("#campo-apellido");
  const campoEmail = document.querySelector("#campo-email");
  const campoCobertura = document.querySelector("#campo-cobertura");
  const campoPassword = document.querySelector("#campo-password");
  const passRequired = document.querySelector("#pass-required");
  const passHelp = document.querySelector("#pass-help");

  const deleteModal = document.querySelector("#delete-modal");
  const deletePatientName = document.querySelector("#delete-patient-name");
  const formDelete = document.querySelector("#form-delete-paciente");

  const toggleModal = (isOpen) => {
    if (!patientModal) return;
    patientModal.hidden = !isOpen;
    document.body.classList.toggle("modal-open", isOpen);
    if (isOpen) {
      campoNombre?.focus();
    }
  };

  const toggleDeleteModal = (isOpen) => {
    if (!deleteModal) return;
    deleteModal.hidden = !isOpen;
    document.body.classList.toggle("modal-open", isOpen);
  };

  document.querySelector("#btn-nuevo-paciente")?.addEventListener("click", () => {
    if (!patientForm) return;
    patientForm.reset();
    patientForm.action = patientForm.dataset.createAction;

    if (modalTitle) modalTitle.textContent = "Nuevo paciente";
    if (campoPassword) campoPassword.required = true;
    if (passRequired) passRequired.hidden = false;
    if (passHelp) passHelp.textContent = "Requerida para la creación de cuenta del paciente.";

    toggleModal(true);
  });

  document.querySelectorAll("[data-edit-patient]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!patientForm) return;
      patientForm.reset();
      patientForm.action = btn.dataset.action;

      if (modalTitle) modalTitle.textContent = "Editar paciente";
      if (campoNombre) campoNombre.value = btn.dataset.nombre || "";
      if (campoApellido) campoApellido.value = btn.dataset.apellido || "";
      if (campoEmail) campoEmail.value = btn.dataset.email || "";
      if (campoCobertura) campoCobertura.value = btn.dataset.coberturaId || "";

      if (campoPassword) {
        campoPassword.value = "";
        campoPassword.required = false;
      }
      if (passRequired) passRequired.hidden = true;
      if (passHelp) passHelp.textContent = "Opcional. Dejar vacío para conservar la contraseña actual.";

      toggleModal(true);
    });
  });

  document.querySelectorAll("[data-delete-patient]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (deletePatientName) deletePatientName.textContent = btn.dataset.name || "este paciente";
      if (formDelete) formDelete.action = btn.dataset.action;
      toggleDeleteModal(true);
    });
  });

  document.querySelectorAll("#btn-cerrar-modal, #btn-cancelar-modal").forEach((btn) => {
    btn.addEventListener("click", () => toggleModal(false));
  });

  document.querySelector("#btn-cancelar-eliminar")?.addEventListener("click", () => {
    toggleDeleteModal(false);
  });

  patientModal?.addEventListener("click", (e) => {
    if (e.target === patientModal) toggleModal(false);
  });

  deleteModal?.addEventListener("click", (e) => {
    if (e.target === deleteModal) toggleDeleteModal(false);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (patientModal && !patientModal.hidden) toggleModal(false);
      if (deleteModal && !deleteModal.hidden) toggleDeleteModal(false);
    }
  });

  searchInput?.addEventListener("input", () => {
    const query = searchInput.value.trim().toLowerCase();
    let matches = 0;

    tableRows.forEach((row) => {
      const rowSearch = (row.dataset.search ?? "").toLowerCase();
      const isMatch = rowSearch.includes(query);
      row.hidden = !isMatch;
      if (isMatch) matches++;
    });

    if (countNum) countNum.textContent = matches;
    if (emptyMsg) emptyMsg.hidden = matches > 0;
  });
})();
