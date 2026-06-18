const pvrCanvas = document.getElementById("pvrChart");
if (pvrCanvas && window.dashboardData) {
  new Chart(pvrCanvas, {
    type: "bar",
    data: {
      labels: window.dashboardData.map((row) => row.model),
      datasets: [{
        label: "PVR per 1k",
        data: window.dashboardData.map((row) => row.pvr),
        backgroundColor: "#27548a"
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true } },
      plugins: { legend: { display: false } }
    }
  });
}
