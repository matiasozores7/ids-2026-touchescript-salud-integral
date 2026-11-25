const data = window.REPORT_DATA || {
  specialties: { labels: [], values: [] },
  appointmentResults: { labels: [], values: [] },
  occupancy: { labels: [], values: [] },
  waiting: { labels: [], values: [] },
  professionals: { labels: [], values: [] },
};

if (typeof Chart === "undefined") {
  console.error("Chart.js no está cargado");
} else {
  Chart.defaults.font.family =
    "'Plus Jakarta Sans', system-ui, -apple-system, sans-serif";
  Chart.defaults.color = "#667085";

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 500 },
  };

  new Chart(document.getElementById("specialtiesChart"), {
    type: "bar",
    data: {
      labels: data.specialties.labels,
      datasets: [{
        data: data.specialties.values,
        backgroundColor: "#d55b66",
        borderRadius: 5,
        barPercentage: 0.8,
      }],
    },
    options: {
      ...commonOptions,
      indexAxis: "y",
      plugins: { legend: { display: false } },
      scales: {
        x: {
          beginAtZero: true,
          ticks: { callback: value => `${value}%` },
          grid: { color: "#edf0f4" },
        },
        y: { grid: { display: false } },
      },
    },
  });

  new Chart(document.getElementById("appointmentsChart"), {
    type: "doughnut",
    data: {
      labels: data.appointmentResults.labels,
      datasets: [{
        data: data.appointmentResults.values,
        backgroundColor: ["#24867e", "#ffb43b", "#d55b66"],
        borderColor: "#ffffff",
        borderWidth: 4,
      }],
    },
    options: {
      ...commonOptions,
      cutout: "58%",
    },
  });

  new Chart(document.getElementById("occupancyChart"), {
    type: "bar",
    data: {
      labels: data.occupancy.labels,
      datasets: [{
        data: data.occupancy.values,
        backgroundColor: "#237faa",
        borderRadius: 7,
      }],
    },
    options: {
      ...commonOptions,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { callback: value => `${value}%` },
          grid: { color: "#edf0f4" },
        },
        x: { grid: { display: false } },
      },
    },
  });

  new Chart(document.getElementById("waitingChart"), {
    type: "line",
    data: {
      labels: data.waiting.labels,
      datasets: [{
        data: data.waiting.values,
        borderColor: "#247c78",
        borderWidth: 2,
        tension: 0.35,
        pointRadius: 0,
        fill: false,
      }],
    },
    options: {
      ...commonOptions,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: value => `${value} min` },
          grid: { color: "#edf0f4" },
        },
        x: { grid: { display: false } },
      },
    },
  });

  new Chart(document.getElementById("professionalsChart"), {
    type: "bar",
    data: {
      labels: data.professionals.labels,
      datasets: [{
        data: data.professionals.values,
        backgroundColor: "#ffb43b",
        borderRadius: 7,
      }],
    },
    options: {
      ...commonOptions,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: value => `${value} min` },
          grid: { color: "#edf0f4" },
        },
        x: { grid: { display: false } },
      },
    },
  });
}