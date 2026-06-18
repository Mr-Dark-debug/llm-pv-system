const analysis = window.analysisData || {};
const scatter = document.getElementById("scatterChart");
if (scatter) {
  new Chart(scatter, {
    type: "scatter",
    data: {
      datasets: [{
        label: "Participants",
        data: (analysis.survey_points || []).map((row) => ({ x: row.lei, y: row.pva })),
        backgroundColor: "#2d7d5f"
      }]
    },
    options: {
      scales: {
        x: { title: { display: true, text: "LEI" }, beginAtZero: true },
        y: { title: { display: true, text: "PVA" }, beginAtZero: true, max: 100 }
      }
    }
  });
}

const pvr = document.getElementById("analysisPvrChart");
if (pvr) {
  new Chart(pvr, {
    type: "bar",
    data: {
      labels: (analysis.model_pvr || []).map((row) => row.model),
      datasets: [{ label: "PVR", data: (analysis.model_pvr || []).map((row) => row.pvr), backgroundColor: "#27548a" }]
    },
    options: { plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
  });
}
