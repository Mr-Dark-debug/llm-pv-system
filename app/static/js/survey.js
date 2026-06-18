function selectedModelValues(form, provider) {
  return Array.from(form.querySelectorAll(`input[name="model_${provider}"]:checked`)).map((item) => item.value);
}

function syncRangeLabels(form) {
  form.querySelectorAll(".live-range").forEach((range) => {
    const output = form.querySelector(`[data-range-value="${range.name}"]`);
    if (output) output.textContent = range.value;
    range.addEventListener("input", () => {
      if (output) output.textContent = range.value;
    });
  });
}

function makePayload(form) {
  const data = new FormData(form);
  const forced = Array.from({ length: 10 }, (_, index) => {
    const item = `D${index + 1}`;
    return { item_id: item, pv_chosen: data.has(`forced_${item}`) };
  });
  const translation = Array.from({ length: 5 }, (_, index) => {
    const item = `E${index + 1}`;
    return {
      item_id: item,
      translated_text: "",
      pv_used: data.has(`translation_${item}`),
      meaning_correct: true,
      score: data.has(`translation_${item}`) ? 2 : 1
    };
  });
  const acceptability = Array.from({ length: 5 }, (_, index) => {
    const item = `F${index + 1}`;
    return { item_id: item, rating: Number(data.get(`accept_${item}`) || 3), pv_variant: true };
  });
  return {
    study: form.dataset.study,
    survey_link_token: form.dataset.linkToken || null,
    demographics: {
      age: Number(data.get("age")),
      gender: data.get("gender"),
      l1_language: data.get("l1_language"),
      l1_family: "other",
      country: data.get("country"),
      education: data.get("education"),
      years_english: Number(data.get("years_english")),
      cefr_self_rating: data.get("cefr_self_rating"),
      attention_checks_passed: 3
    },
    usage: {
      chatgpt_frequency: Number(data.get("chatgpt_frequency")),
      chatgpt_models: selectedModelValues(form, "openai"),
      claude_frequency: Number(data.get("claude_frequency")),
      claude_models: selectedModelValues(form, "anthropic"),
      gemini_frequency: Number(data.get("gemini_frequency")),
      gemini_models: selectedModelValues(form, "google"),
      daily_minutes_llm: Number(data.get("daily_minutes_llm")),
      duration_of_use_months: Number(data.get("duration_of_use_months")),
      noticing_c7: 4,
      noticing_c8: true,
      noticing_c10: 4,
      purpose_grammar: true,
      purpose_vocab: true,
      purpose_translation: true,
      purpose_writing: true
    },
    tasks: { forced_choice: forced, translation, acceptability },
    qualitative: {
      qualitative_g1: data.get("qualitative_g1"),
      qualitative_g2: data.get("qualitative_g2")
    }
  };
}

function initializeSurvey(form) {
  const steps = Array.from(form.querySelectorAll(".survey-step"));
  const progress = document.getElementById("surveyProgress");
  const back = document.getElementById("surveyBack");
  const next = document.getElementById("surveyNext");
  const dots = document.getElementById("surveyDots");
  const result = document.getElementById("surveyResult");
  let index = 0;

  dots.innerHTML = steps.map((_, dotIndex) => `<span data-dot="${dotIndex}"></span>`).join("");
  syncRangeLabels(form);

  function render() {
    steps.forEach((step, stepIndex) => step.classList.toggle("active", stepIndex === index));
    dots.querySelectorAll("span").forEach((dot, dotIndex) => dot.classList.toggle("active", dotIndex === index));
    progress.style.width = `${((index + 1) / steps.length) * 100}%`;
    back.disabled = index === 0;
    next.textContent = index === steps.length - 1 ? "Submit" : "Continue";
  }

  back.addEventListener("click", () => {
    index = Math.max(index - 1, 0);
    render();
  });

  next.addEventListener("click", async () => {
    if (index < steps.length - 1) {
      index += 1;
      render();
      return;
    }
    next.disabled = true;
    next.textContent = "Saving...";
    const response = await fetch("/api/survey/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(makePayload(form))
    });
    if (response.ok) {
      const payload = await response.json();
      result.hidden = false;
      result.innerHTML = `<strong>Recorded.</strong><small>Your anonymous code is ${payload.participant_code}. Thank you for helping the study.</small>`;
      next.textContent = "Saved";
    } else {
      const payload = await response.json().catch(() => ({ detail: "Submission failed" }));
      result.hidden = false;
      result.innerHTML = `<strong>Could not save.</strong><small>${payload.detail || "Please check the form and try again."}</small>`;
      next.disabled = false;
      next.textContent = "Try again";
    }
  });

  form.querySelectorAll(".choice-card, .model-pill, .chip-check").forEach((card) => {
    card.addEventListener("change", () => card.classList.toggle("selected", card.querySelector("input")?.checked));
    card.classList.toggle("selected", card.querySelector("input")?.checked);
  });

  render();
}

const surveyForm = document.getElementById("surveyForm");
if (surveyForm) initializeSurvey(surveyForm);
