const searchInput = document.querySelector("#buscar-paciente");
const tableBody = document.querySelector("#pacientes-table-body");
const countNum = document.querySelector("#pacientes-count-num");
const emptyMsg = document.querySelector("#pacientes-table-empty");
const modal = document.querySelector("#patient-modal");
const modalTitle = document.querySelector("#patient-modal-title");
const form = document.querySelector("#form-paciente");

let selectedRow = null;

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

document.querySelector("#btn-nuevo-paciente")?.addEventListener("click", () => toggleModal(true));
document.querySelectorAll("#btn-cerrar-modal, #btn-cancelar-modal").forEach((btn) => {
  btn.addEventListener("click", () => toggleModal(false));
});
modal?.addEventListener("click", (e) => { if (e.target === modal) toggleModal(false); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !modal.hidden) toggleModal(false); });

tableBody?.addEventListener("click", (e) => {
  const row = e.target.closest("tr");
  if (!row) return;

  if (e.target.closest("[data-edit-patient]")) {
    toggleModal(true, row);
  } else if (e.target.closest("[data-delete-patient]")) {
    if (confirm(`¿Dar de baja al paciente ${row.dataset.nombre} ${row.dataset.apellido}?`)) {
      row.remove();
      actualizarVisibles();
    }
  }
});

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
