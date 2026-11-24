
(() => {
    "use strict";

    // ========================================
    // DATOS
    // ========================================

    const appointments = window.CALENDAR_DATA?.turnos || [];

    // ========================================
    // ELEMENTOS
    // ========================================

    const board = document.getElementById("calendar-board");
    const emptyState = document.getElementById("calendar-empty");
    const dateRange = document.getElementById("calendar-date-range");

    const previousButton = document.getElementById("calendar-previous");
    const nextButton = document.getElementById("calendar-next");
    const todayButton = document.getElementById("calendar-today");

    const specialtyFilter = document.getElementById(
        "calendar-filter-specialty"
    );

    const doctorFilter = document.getElementById(
        "calendar-filter-doctor"
    );

    const showCancelledFilter = document.getElementById(
        "calendar-show-cancelled"
    );

    const modalElement = document.getElementById(
        "calendar-appointment-modal"
    );

    // ========================================
    // ESTADO
    // ========================================

    const statusLabels = {
        disponible: "Disponible",
        reservado: "Reservado",
        confirmado: "Confirmado",
        atendido: "Atendido",
        cancelado: "Cancelado",
        ausente: "Ausente"
    };

    const allowedStatuses = new Set(Object.keys(statusLabels));

    const dayFormatter = new Intl.DateTimeFormat("es-AR", {
        weekday: "long"
    });

    const dateFormatter = new Intl.DateTimeFormat("es-AR", {
        day: "numeric",
        month: "long"
    });

    const monthFormatter = new Intl.DateTimeFormat("es-AR", {
        month: "long"
    });

    // ========================================
    // SEGURIDAD
    // ========================================

    function escapeHTML(value) {
        return String(value ?? "").replace(/[&<>"']/g, character => {
            const entities = {
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"
            };

            return entities[character];
        });
    }

    // ========================================
    // FECHAS
    // ========================================

    function parseLocalDate(dateString) {
        const [year, month, day] = dateString.split("-").map(Number);

        return new Date(year, month - 1, day);
    }

    function formatDateKey(date) {
        return [
            date.getFullYear(),
            String(date.getMonth() + 1).padStart(2, "0"),
            String(date.getDate()).padStart(2, "0")
        ].join("-");
    }

    function getWeekDates() {
        const monday = parseLocalDate(
            window.CALENDAR_DATA.fechaInicio
        );

        return Array.from({ length: 6 }, (_, index) => {
            const date = new Date(monday);

            date.setDate(monday.getDate() + index);

            return date;
        });
    }

    function formatDateRange(dates) {
        const first = dates[0];
        const last = dates[5];

        if (first.getMonth() === last.getMonth()) {
            return `${first.getDate()} – ${last.getDate()} de ${monthFormatter.format(last)} de ${last.getFullYear()}`;
        }

        return `${dateFormatter.format(first)} – ${dateFormatter.format(last)} de ${last.getFullYear()}`;
    }

    function isToday(date) {
        const today = new Date();

        return formatDateKey(date) === formatDateKey(today);
    }

    // ========================================
    // NAVEGACIÓN
    // ========================================

    function navigateWeek(offset) {
        const monday = getWeekDates()[0];

        monday.setDate(monday.getDate() + offset * 7);

        const params = new URLSearchParams(window.location.search);

        params.set("fecha_inicio", formatDateKey(monday));

        window.location.search = params.toString();
    }

    function navigateToToday() {
        const params = new URLSearchParams(window.location.search);

        params.delete("fecha_inicio");

        window.location.search = params.toString();
    }

    // ========================================
    // FILTROS
    // ========================================

    function populateFilter(select, placeholder, items) {
        const selectedValue = select.value;

        select.innerHTML = "";

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = placeholder;

        select.appendChild(defaultOption);

        items.forEach(item => {
            const option = document.createElement("option");

            option.value = String(item.id);
            option.textContent = item.name;

            select.appendChild(option);
        });

        if (
            Array.from(select.options).some(
                option => option.value === selectedValue
            )
        ) {
            select.value = selectedValue;
        }
    }

    function initializeFilters() {
        populateFilter(
            specialtyFilter,
            "Todas las especialidades",
            window.CALENDAR_DATA?.especialidades || []
        );

        populateFilter(
            doctorFilter,
            "Todos los profesionales",
            window.CALENDAR_DATA?.medicos || []
        );
    }

    // ========================================
    // FILTRADO
    // ========================================

    function getFilteredAppointments(day) {
        const dateKey = formatDateKey(getWeekDates()[day]);

        return appointments
            .filter(appointment => {
                if (appointment.dateKey !== dateKey) {
                    return false;
                }

                if (
                    specialtyFilter.value &&
                    String(appointment.specialtyId) !== specialtyFilter.value
                ) {
                    return false;
                }

                if (
                    doctorFilter.value &&
                    String(appointment.doctorId) !== doctorFilter.value
                ) {
                    return false;
                }

                if (
                    !showCancelledFilter.checked &&
                    appointment.status === "cancelado"
                ) {
                    return false;
                }

                return true;
            })
            .sort((a, b) => a.time.localeCompare(b.time));
    }

    // ========================================
    // TARJETAS
    // ========================================

    function createAppointmentCard(appointment) {
        const statusClass = allowedStatuses.has(appointment.status)
            ? `status-${appointment.status}`
            : "";

        return `
            <button
                type="button"
                class="calendar-appointment ${statusClass}"
                data-appointment-id="${escapeHTML(appointment.id)}"
                aria-label="Turno de ${escapeHTML(appointment.patient)}, ${escapeHTML(appointment.time)}"
            >
                <span class="calendar-appointment-time">
                    ${escapeHTML(appointment.time)}
                </span>

                <span class="calendar-appointment-patient">
                    ${escapeHTML(appointment.patient)}
                </span>

                <span class="calendar-appointment-doctor">
                    ${escapeHTML(appointment.doctor)}
                </span>

                <span class="calendar-appointment-specialty">
                    ${escapeHTML(appointment.specialty)}
                </span>
            </button>
        `;
    }

    // ========================================
    // DÍAS
    // ========================================

    function createDayColumn(date, dayIndex) {
        const dayAppointments = getFilteredAppointments(dayIndex);

        const dayName = dayFormatter.format(date);
        const formattedDay = dayName.charAt(0).toUpperCase() +
            dayName.slice(1);

        const todayClass = isToday(date) ? "is-today" : "";

        const appointmentsHTML = dayAppointments.length
            ? dayAppointments.map(createAppointmentCard).join("")
            : `
                <div class="calendar-day-empty">
                    Sin turnos programados
                </div>
            `;

        return `
            <article class="calendar-day ${todayClass}">

                <header class="calendar-day-header">

                    <span class="calendar-day-name">
                        ${formattedDay}
                    </span>

                    <div class="calendar-day-date">

                        <strong>${date.getDate()}</strong>

                        <span class="calendar-day-count">
                            ${dayAppointments.length}
                            ${dayAppointments.length === 1 ? "turno" : "turnos"}
                        </span>

                    </div>

                </header>

                <div class="calendar-day-appointments">
                    ${appointmentsHTML}
                </div>

            </article>
        `;
    }

    // ========================================
    // RENDERIZADO
    // ========================================

    function renderCalendar() {
        const dates = getWeekDates();

        dateRange.textContent = formatDateRange(dates);

        const totalAppointments = dates.reduce((total, _, index) => {
            return total + getFilteredAppointments(index).length;
        }, 0);

        board.innerHTML = dates
            .map((date, index) => createDayColumn(date, index))
            .join("");

        const hasAppointments = totalAppointments > 0;

        board.hidden = !hasAppointments;
        emptyState.hidden = hasAppointments;

        if (hasAppointments) {
            bindAppointmentEvents();
        }
    }

    // ========================================
    // DETALLE DEL TURNO
    // ========================================

    function showAppointmentDetails(appointmentId) {
        const appointment = appointments.find(
            item => String(item.id) === String(appointmentId)
        );

        if (!appointment) {
            return;
        }

        const date = parseLocalDate(appointment.dateKey);

        document.getElementById("calendar-detail-patient").textContent =
            appointment.patient;

        document.getElementById("calendar-detail-doctor").textContent =
            appointment.doctor;

        document.getElementById("calendar-detail-specialty").textContent =
            appointment.specialty;

        document.getElementById("calendar-detail-datetime").textContent =
            `${dateFormatter.format(date)} · ${appointment.time}`;

        document.getElementById("calendar-detail-office").textContent =
            appointment.office;

        document.getElementById("calendar-detail-status").textContent =
            statusLabels[appointment.status] || appointment.status;

        if (window.bootstrap?.Modal) {
            bootstrap.Modal
                .getOrCreateInstance(modalElement)
                .show();
        }
    }

    function bindAppointmentEvents() {
        board.querySelectorAll("[data-appointment-id]").forEach(button => {
            button.addEventListener("click", () => {
                showAppointmentDetails(
                    button.dataset.appointmentId
                );
            });
        });
    }

    // ========================================
    // EVENTOS
    // ========================================

    previousButton.addEventListener("click", () => {
        navigateWeek(-1);
    });

    nextButton.addEventListener("click", () => {
        navigateWeek(1);
    });

    todayButton.addEventListener("click", navigateToToday);

    specialtyFilter.addEventListener("change", renderCalendar);
    doctorFilter.addEventListener("change", renderCalendar);

    showCancelledFilter.addEventListener("change", renderCalendar);


    // ========================================
    // INICIALIZACIÓN
    // ========================================

    initializeFilters();
    renderCalendar();

})();
