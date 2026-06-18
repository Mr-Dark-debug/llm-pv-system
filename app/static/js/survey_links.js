const linkForm = document.getElementById("surveyLinkForm");
const linkBox = document.getElementById("newLinkBox");

linkForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(linkForm);
  const response = await fetch("/api/survey/links", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      label: data.get("label"),
      study: data.get("study"),
      condition: data.get("condition") || null
    })
  });
  const payload = await response.json();
  if (!response.ok) {
    linkBox.hidden = false;
    linkBox.textContent = payload.detail || "Could not create link.";
    return;
  }
  linkBox.hidden = false;
  linkBox.innerHTML = `<strong>Share link ready</strong><code>${payload.url}</code><button class="btn btn-sm btn-light" type="button">Copy</button>`;
  const button = linkBox.querySelector("button");
  button.addEventListener("click", async () => {
    await navigator.clipboard.writeText(payload.url);
    button.textContent = "Copied";
  });
});
