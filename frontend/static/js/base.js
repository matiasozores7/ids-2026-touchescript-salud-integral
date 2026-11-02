const specialtySelect = document.querySelector('select[name="especialidad"]');
const doctorSelect = document.querySelector("#doctor-filter");

if (specialtySelect && doctorSelect) {
  const filterDoctors = () => {
    const specialtyId = specialtySelect.value;

    for (const option of doctorSelect.options) {
      if (option.value) {
        option.hidden = Boolean(specialtyId && option.dataset.specialty !== specialtyId);
      }
    }

    if (doctorSelect.selectedOptions[0]?.hidden) {
      doctorSelect.value = "";
    }
  };

  specialtySelect.addEventListener("change", filterDoctors);
  filterDoctors();
}
