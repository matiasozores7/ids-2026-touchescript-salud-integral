
(() => {
    "use strict";

    // ========================================
    // DATOS FICTICIOS
    // day: 0 = lunes ... 5 = sábado
    // ========================================

    const appointments = [
        {
            id: 1,
            day: 0,
            time: "08:00",
            patient: "Sofía Martínez",
            doctor: "María González",
            specialty: "Cardiología",
            office: "101",
            status: "confirmado"
        },
        {
            id: 2,
            day: 0,
            time: "09:00",
            patient: "Lucas Fernández",
            doctor: "Juan Pérez",
            specialty: "Clínica médica",
            office: "102",
            status: "reservado"
        },
        {
            id: 3,
            day: 0,
            time: "10:30",
            patient: "Valentina López",
            doctor: "Laura Fernández",
            specialty: "Dermatología",
            office: "103",
            status: "atendido"
        },
        {
            id: 4,
            day: 1,
            time: "08:30",
            patient: "Tomás Rodríguez",
            doctor: "Carlos Rodríguez",
            specialty: "Traumatología",
            office: "104",
            status: "confirmado"
        },
        {
            id: 5,
            day: 1,
            time: "10:00",
            patient: "Camila Torres",
            doctor: "María González",
            specialty: "Cardiología",
            office: "101",
            status: "cancelado"
        },
        {
            id: 6,
            day: 1,
            time: "11:30",
            patient: "Mateo García",
            doctor: "Juan Pérez",
            specialty: "Clínica médica",
            office: "102",
            status: "confirmado"
        },
        {
            id: 7,
            day: 2,
            time: "09:00",
            patient: "Martina Díaz",
            doctor: "Laura Fernández",
            specialty: "Dermatología",
            office: "103",
            status: "reservado"
        },
        {
            id: 8,
            day: 2,
            time: "11:00",
            patient: "Benjamín Castro",
            doctor: "Carlos Rodríguez",
            specialty: "Traumatología",
            office: "104",
            status: "ausente"
        },
        {
            id: 9,
            day: 3,
            time: "08:00",
            patient: "Emma Romero",
            doctor: "María González",
            specialty: "Cardiología",
            office: "101",
            status: "confirmado"
        },
        {
            id: 10,
            day: 3,
            time: "10:30",
            patient: "Joaquín Herrera",
            doctor: "Juan Pérez",
            specialty: "Clínica médica",
            office: "102",
            status: "reservado"
        },
        {
            id: 11,
            day: 4,
            time: "09:30",
            patient: "Isabella Morales",
            doctor: "Laura Fernández",
            specialty: "Dermatología",
            office: "103",
            status: "confirmado"
        },
        {
            id: 12,
            day: 4,
            time: "11:00",
            patient: "Santiago Acosta",
            doctor: "Carlos Rodríguez",
            specialty: "Traumatología",
            office: "104",
            status: "cancelado"
        },
        {
            id: 13,
            day: 5,
            time: "09:00",
            patient: "Renata Silva",
            doctor: "María González",
            specialty: "Cardiología",
            office: "101",
            status: "confirmado"
        }
    ];

    // ========================================
    // ELEMENTOS
    // ========================================

    const board = document.getElementById("calendar-board");
    const emptyState = document.getElementById("calendar-empty");
    const dateRange = document.getElementById("calendar-date-range");

    const previousButton = document.getElementById("calendar-previous");
    const nextButton = document.getElementById("calendar-next");
    const todayButton = document.getElementById("calendar-today");
    const newAppointmentButton = document.getElementById("calendar-new-appointment");

    const specialtyFilter = document.getElementById("calendar-filter-specialty");
    const doctorFilter = document.getElementById("calendar-filter-doctor");
    const showCancelledFilter = document.getElementById("calendar-show-cancelled");

    const modalElement = document.getElementById("calendar-appointment-modal");

    // ========================================
    // ESTADO
    // ========================================

    let weekOffset = 0;

    const statusLabels = {
        reservado: "Reservado",
        confirmado: "Confirmado",
        atendido: "Atendido",
        cancelado: "Cancelado",
        ausente: "Ausente"
    };

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
    // FECHAS
    // ========================================

    function getMonday(date) {
        const result = new Date(
            date.getFullYear(),
            date.getMonth(),
            date.getDate()
        );

        const day = result.getDay();
        const difference = day === 0 ? -6 : 1 - day;

        result.setDate(result.getDate() + difference);

        return result;
    }

    function getWeekDates() {
        const today = new Date();
        const monday = getMonday(today);

        monday.setDate(monday.getDate() + weekOffset * 7);

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

        return (
            date.getDate() === today.getDate() &&
            date.getMonth() === today.getMonth() &&
            date.getFullYear() === today.getFullYear()
        );
    }

    // ========================================
    // FILTROS
    // ========================================

    function getFilteredAppointments(day) {
        return appointments
            .filter(appointment => {
                if (appointment.day !== day) {
                    return false;
                }

                if (
                    specialtyFilter.value &&
                    appointment.specialty !== specialtyFilter.value
                ) {
                    return false;
                }

                if (
                    doctorFilter.value &&
                    appointment.doctor !== doctorFilter.value
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
        return `
            <button
                type="button"
                class="calendar-appointment status-${appointment.status}"
                data-appointment-id="${appointment.id}"
                aria-label="Turno de ${appointment.patient}, ${appointment.time}"
            >
                <span class="calendar-appointment-time">
                    ${appointment.time}
                </span>

                <span class="calendar-appointment-patient">
                    ${appointment.patient}
                </span>

                <span class="calendar-appointment-doctor">
                    Dr./Dra. ${appointment.doctor}
                </span>

                <span class="calendar-appointment-specialty">
                    ${appointment.specialty}
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
        const formattedDay = dayName.charAt(0).toUpperCase() + dayName.slice(1);

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
            item => item.id === Number(appointmentId)
        );

        if (!appointment) {
            return;
        }

        const date = getWeekDates()[appointment.day];

        document.getElementById("calendar-detail-patient").textContent =
            appointment.patient;

        document.getElementById("calendar-detail-doctor").textContent =
            `Dr./Dra. ${appointment.doctor}`;

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
                showAppointmentDetails(button.dataset.appointmentId);
            });
        });
    }

    // ========================================
    // EVENTOS
    // ========================================

    previousButton.addEventListener("click", () => {
        weekOffset--;
        renderCalendar();
    });

    nextButton.addEventListener("click", () => {
        weekOffset++;
        renderCalendar();
    });

    todayButton.addEventListener("click", () => {
        weekOffset = 0;
        renderCalendar();
    });

    specialtyFilter.addEventListener("change", renderCalendar);
    doctorFilter.addEventListener("change", renderCalendar);
    showCancelledFilter.addEventListener("change", renderCalendar);

    newAppointmentButton.addEventListener("click", () => {
        window.alert(
            "La creación de turnos se implementará durante la etapa de integración."
        );
    });

    // ========================================
    // INICIALIZACIÓN
    // ========================================

    renderCalendar();

})();
