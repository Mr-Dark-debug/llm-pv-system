function showStatus(message, isError = false) {
  const container = document.getElementById("benchmarkStatus");
  const item = document.createElement("div");
  item.className = `toast show text-bg-${isError ? "danger" : "success"}`;
  item.innerHTML = `<div class="toast-body">${message}</div>`;
  container.appendChild(item);
  setTimeout(() => item.remove(), 5000);
}

document.querySelectorAll(".run-model").forEach((button) => {
  button.addEventListener("click", async () => {
    button.disabled = true;
    const modelId = button.dataset.modelId;
    try {
      const response = await fetch(`/api/benchmark/run/${modelId}?prompt_limit=5`, { method: "POST" });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Benchmark failed");
      showStatus(`Created ${payload.responses_created} responses; PVR ${payload.pvr_overall}`);
      setTimeout(() => window.location.reload(), 800);
    } catch (error) {
      showStatus(error.message, true);
    } finally {
      button.disabled = false;
    }
  });
});
