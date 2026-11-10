const searchInput = document.querySelector("#buscar-paciente");
const tableBody = document.querySelector("#pacientes-table-body");
const countNum = document.querySelector("#pacientes-count-num");
const emptyMsg = document.querySelector("#pacientes-table-empty");
const modal = document.querySelector("#patient-modal");
const modalTitle = document.querySelector("#patient-modal-title");
const form = document.querySelector("#form-paciente");

// Referencias del Popup Modal de eliminación
const deleteModal = document.querySelector("#delete-modal");
const deletePatientName = document.querySelector("#delete-patient-name");
const btnCancelarEliminar = document.querySelector("#btn-cancelar-eliminar");
const btnConfirmarEliminar = document.querySelector("#btn-confirmar-eliminar");

let selectedRow = null;
let rowToDelete = null;

// Control del modal de alta / edición
const toggleModal = (isOpen, row = null) => {
  modal.hidden = !isOpen;
  document.body.classList.toggle("modal-open", isOpen);
  if (!isOpen) return;

  selectedRow = row;
  modalTitle.textContent = row ? "Editar paciente" : "Nuevo paciente";
  form.reset();

  if (row) {
    form.elements["id"].value = row.dataset.id || "";
    form.elements["nombre"].value = row.dataset.nombre || "";
    form.elements["apellido"].value = row.dataset.apellido || "";
    form.elements["dni"].value = row.dataset.dni || "";
    form.elements["fecha_nacimiento"].value = row.dataset.fecha || "";
    form.elements["email"].value = row.dataset.email || "";
    form.elements["telefono"].value = row.dataset.telefono || "";
    form.elements["cobertura"].value = row.dataset.cobertura || "";
    form.elements["nro_afiliado"].value = row.dataset.afiliado || "";
  }
  form.elements["nombre"]?.focus();
};

// Control del popup modal de confirmación de eliminación
const toggleDeleteModal = (isOpen, row = null) => {
  if (!deleteModal) return;
  deleteModal.hidden = !isOpen;
  document.body.classList.toggle("modal-open", isOpen);
  rowToDelete = isOpen ? row : null;

  if (isOpen && row && deletePatientName) {
    deletePatientName.textContent = `${row.dataset.nombre || ""} ${row.dataset.apellido || ""}`.trim();
  }
};

// Listeners de apertura y cierre de modales
document.querySelector("#btn-nuevo-paciente")?.addEventListener("click", () => toggleModal(true));
document.querySelectorAll("#btn-cerrar-modal, #btn-cancelar-modal").forEach((btn) => {
  btn.addEventListener("click", () => toggleModal(false));
});
btnCancelarEliminar?.addEventListener("click", () => toggleDeleteModal(false));

modal?.addEventListener("click", (e) => { if (e.target === modal) toggleModal(false); });
deleteModal?.addEventListener("click", (e) => { if (e.target === deleteModal) toggleDeleteModal(false); });

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    if (!modal.hidden) toggleModal(false);
    if (deleteModal && !deleteModal.hidden) toggleDeleteModal(false);
  }
});

// Confirmar baja de paciente en el popup modal
btnConfirmarEliminar?.addEventListener("click", () => {
  if (rowToDelete) {
    rowToDelete.remove();
    actualizarVisibles();
  }
  toggleDeleteModal(false);
});

// Acciones en la tabla: Editar y Eliminar
tableBody?.addEventListener("click", (e) => {
  const row = e.target.closest("tr");
  if (!row) return;

  if (e.target.closest("[data-edit-patient]")) {
    toggleModal(true, row);
  } else if (e.target.closest("[data-delete-patient]")) {
    toggleDeleteModal(true, row);
  }
});

// Guardar formulario en interfaz (alta y edición seguras con cloneNode y textContent, sin innerHTML)
form?.addEventListener("submit", (e) => {
  e.preventDefault();

  const nombre = form.elements["nombre"].value.trim();
  const apellido = form.elements["apellido"].value.trim();
  const dni = form.elements["dni"].value.trim();
  const email = form.elements["email"].value.trim();
  const tel = form.elements["telefono"].value.trim();
  const cob = form.elements["cobertura"].value;
  const fecha = form.elements["fecha_nacimiento"].value;
  const afiliado = form.elements["nro_afiliado"].value.trim();
  const iniciales = ((nombre[0] || "") + (apellido[0] || "")).toUpperCase();
  const searchStr = `${nombre} ${apellido} ${dni} ${email} ${cob}`.toLowerCase();

  if (selectedRow) {
    // Modo Edición: actualiza fila existente
    selectedRow.dataset.nombre = nombre;
    selectedRow.dataset.apellido = apellido;
    selectedRow.dataset.dni = dni;
    selectedRow.dataset.fecha = fecha;
    selectedRow.dataset.email = email;
    selectedRow.dataset.telefono = tel;
    selectedRow.dataset.cobertura = cob;
    selectedRow.dataset.afiliado = afiliado;
    selectedRow.dataset.search = searchStr;

    const avatar = selectedRow.querySelector(".patient-avatar");
    if (avatar) avatar.textContent = iniciales;

    const nameEl = selectedRow.querySelector(".patient-name");
    if (nameEl) nameEl.textContent = `${nombre} ${apellido}`;

    const emailEl = selectedRow.querySelector(".patient-email");
    if (emailEl) emailEl.textContent = email;

    const cells = selectedRow.querySelectorAll("td");
    if (cells[1]) cells[1].textContent = dni;
    if (cells[2]) cells[2].textContent = tel || "-";
    if (cells[3]) cells[3].textContent = cob;
  } else {
    // Modo Alta: clonamos una fila existente (cero innerHTML)
    const plantilla = tableBody?.querySelector("tr");
    if (plantilla) {
      const nuevaFila = plantilla.cloneNode(true);
      nuevaFila.dataset.id = Date.now();
      nuevaFila.dataset.nombre = nombre;
      nuevaFila.dataset.apellido = apellido;
      nuevaFila.dataset.dni = dni;
      nuevaFila.dataset.fecha = fecha;
      nuevaFila.dataset.email = email;
      nuevaFila.dataset.telefono = tel;
      nuevaFila.dataset.cobertura = cob;
      nuevaFila.dataset.afiliado = afiliado;
      nuevaFila.dataset.search = searchStr;
      nuevaFila.hidden = false;

      const avatar = nuevaFila.querySelector(".patient-avatar");
      if (avatar) {
        avatar.className = "patient-avatar avatar-teal";
        avatar.textContent = iniciales;
      }

      const nameEl = nuevaFila.querySelector(".patient-name");
      if (nameEl) nameEl.textContent = `${nombre} ${apellido}`;

      const emailEl = nuevaFila.querySelector(".patient-email");
      if (emailEl) emailEl.textContent = email;

      const cells = nuevaFila.querySelectorAll("td");
      if (cells[1]) cells[1].textContent = dni;
      if (cells[2]) cells[2].textContent = tel || "-";
      if (cells[3]) cells[3].textContent = cob;
      if (cells[4]) cells[4].textContent = "0";

      tableBody?.prepend(nuevaFila);
      actualizarVisibles();
    }
  }

  toggleModal(false);
});

// Buscador en tiempo real y contador de registros
const actualizarVisibles = () => {
  const rows = Array.from(tableBody?.querySelectorAll("tr") || []);
  const visibles = rows.filter((r) => !r.hidden).length;
  if (countNum) countNum.textContent = visibles;
  if (emptyMsg) emptyMsg.hidden = visibles.length > 0;
};

searchInput?.addEventListener("input", (e) => {
  const query = e.target.value.trim().toLowerCase();
  tableBody?.querySelectorAll("tr").forEach((row) => {
    row.hidden = !(row.dataset.search || "").includes(query);
  });
  actualizarVisibles();
});
