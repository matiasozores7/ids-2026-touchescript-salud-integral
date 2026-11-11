
const searchInput = document.querySelector("#buscar-paciente");
const tableBody = document.querySelector("#pacientes-table-body");
const countNum = document.querySelector("#pacientes-count-num");
const emptyMsg = document.querySelector("#pacientes-table-empty");

const modal = document.querySelector("#patient-modal");
const modalTitle = document.querySelector("#patient-modal-title");
const form = document.querySelector("#form-paciente");

const deleteModal = document.querySelector("#delete-modal");
const deletePatientName = document.querySelector("#delete-patient-name");
const btnCancelarEliminar = document.querySelector("#btn-cancelar-eliminar");
const btnConfirmarEliminar = document.querySelector("#btn-confirmar-eliminar");

let selectedRow = null;
let rowToDelete = null;

// Actualiza el estado visual de los modales.
const actualizarEstadoModal = () => {
  const modalAbierto = (modal && !modal.hidden) ||
                       (deleteModal && !deleteModal.hidden);

  document.body.classList.toggle("modal-open", Boolean(modalAbierto));
};

// Modal de alta y edición.
const toggleModal = (isOpen, row = null) => {
  if (!modal || !form) return;

  modal.hidden = !isOpen;
  selectedRow = isOpen ? row : null;

  if (!isOpen) {
    actualizarEstadoModal();
    return;
  }

  form.reset();

  const esEdicion = Boolean(row);

  modalTitle.textContent = esEdicion ? "Editar paciente" : "Nuevo paciente";

  form.action = esEdicion
    ? `/backoffice/pacientes/${row.dataset.id}/editar`
    : "/backoffice/pacientes";

  form.method = "POST";

  form.elements["nombre"].value = row?.dataset.nombre || "";
  form.elements["apellido"].value = row?.dataset.apellido || "";
  form.elements["email"].value = row?.dataset.email || "";
  form.elements["telefono"].value = row?.dataset.telefono || "";
  form.elements["cobertura_id"].value = row?.dataset.coberturaId || "";

  const passwordInput = form.elements["password"];

  if (passwordInput) {
    passwordInput.required = !esEdicion;
    passwordInput.value = "";
  }

  form.elements["nombre"]?.focus();

  actualizarEstadoModal();
};

// Modal de confirmación de baja.
const toggleDeleteModal = (isOpen, row = null) => {
  if (!deleteModal) return;

  deleteModal.hidden = !isOpen;
  rowToDelete = isOpen ? row : null;

  if (isOpen && row && deletePatientName) {
    deletePatientName.textContent =
      `${row.dataset.nombre || ""} ${row.dataset.apellido || ""}`.trim();
  }

  actualizarEstadoModal();
};

// Apertura y cierre de modales.
document.querySelector("#btn-nuevo-paciente")
  ?.addEventListener("click", () => toggleModal(true));

document.querySelectorAll("#btn-cerrar-modal, #btn-cancelar-modal")
  .forEach(btn => btn.addEventListener("click", () => toggleModal(false)));

btnCancelarEliminar?.addEventListener("click", () => {
  toggleDeleteModal(false);
});

modal?.addEventListener("click", e => {
  if (e.target === modal) toggleModal(false);
});

deleteModal?.addEventListener("click", e => {
  if (e.target === deleteModal) toggleDeleteModal(false);
});

document.addEventListener("keydown", e => {
  if (e.key === "Escape") {
    if (modal && !modal.hidden) toggleModal(false);
    if (deleteModal && !deleteModal.hidden) toggleDeleteModal(false);
  }
});

// Acciones de la tabla.
tableBody?.addEventListener("click", e => {
  const row = e.target.closest("tr");
  if (!row) return;

  if (e.target.closest("[data-edit-patient]")) {
    toggleModal(true, row);
  }

  if (e.target.closest("[data-delete-patient]")) {
    toggleDeleteModal(true, row);
  }
});

// Confirmación de baja: envía un POST real al backend.
btnConfirmarEliminar?.addEventListener("click", () => {
  if (!rowToDelete) return;

  const deleteForm = document.createElement("form");

  deleteForm.method = "POST";
  deleteForm.action =
    `/backoffice/pacientes/${rowToDelete.dataset.id}/eliminar`;

  document.body.appendChild(deleteForm);
  deleteForm.submit();
});

// Buscador y contador.
const actualizarVisibles = () => {
  const rows = Array.from(tableBody?.querySelectorAll("tr") || []);
  const visibles = rows.filter(row => !row.hidden).length;

  if (countNum) countNum.textContent = visibles;
  if (emptyMsg) emptyMsg.hidden = visibles > 0;
};

searchInput?.addEventListener("input", e => {
  const query = e.target.value.trim().toLowerCase();

  tableBody?.querySelectorAll("tr").forEach(row => {
    row.hidden = !(row.dataset.search || "").includes(query);
  });

  actualizarVisibles();
});

actualizarVisibles();
