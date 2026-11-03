document.addEventListener("DOMContentLoaded", () => {
  const modal = document.querySelector("#agenda-modal");
  const openButton = document.querySelector("#new-agenda-button");
  const closeButton = document.querySelector("#close-agenda-modal");
  const cancelButton = document.querySelector("#cancel-agenda");
  const form = document.querySelector("#agenda-form");
  const preview = document.querySelector("#turn-preview");
  const count = document.querySelector("#turn-count");

  function openModal() {
    if (modal) modal.hidden = false;
  }

  function closeModal() {
    if (modal) modal.hidden = true;
  }

  openButton?.addEventListener("click", openModal);
  closeButton?.addEventListener("click", closeModal);
  cancelButton?.addEventListener("click", closeModal);

  modal?.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
  });

  function updatePreview() {
    const start = form?.hora_inicio.value;
    const end = form?.hora_fin.value;
    const duration = Number(form?.duracion_turno.value);

    if (!start || !end || !duration) return;

    const toMinutes = (time) => {
      const [hours, minutes] = time.split(":").map(Number);
      return hours * 60 + minutes;
    };

    const toTime = (minutes) =>
      `${String(Math.floor(minutes / 60)).padStart(2, "0")}:${String(
        minutes % 60
      ).padStart(2, "0")}`;

    const total = Math.max(
      0,
      Math.floor((toMinutes(end) - toMinutes(start)) / duration)
    );

    count.textContent = total;
    preview.innerHTML = "";

    for (let index = 0; index < total; index += 1) {
      const tag = document.createElement("span");
      tag.textContent = toTime(toMinutes(start) + index * duration);
      preview.appendChild(tag);
    }
  }

  form?.querySelectorAll("input").forEach((input) => {
    input.addEventListener("input", updatePreview);
  });

  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    closeModal();
    alert("Bloque de agenda guardado correctamente.");
  });

  document.querySelectorAll(".professional").forEach((professional) => {
    professional.addEventListener("click", () => {
      document.querySelector(".professional.active")?.classList.remove("active");
      professional.classList.add("active");

      const medicoId = professional.dataset.medicoId;
      window.location.href = `/backoffice/agendas/${medicoId}`;
    });
  });

  updatePreview();
});