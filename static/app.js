const sections = [
  "experiences",
  "educations",
  "skills",
  "languages",
  "certifications",
  "projects",
  "links",
];

function addItem(section) {
  const container = document.querySelector(`[data-section="${section}"]`);
  const template = document.getElementById(`template-${section}`);
  if (!container || !template) return;

  const fragment = template.content.cloneNode(true);
  const item = fragment.querySelector(".item");
  const removeBtn = fragment.querySelector("[data-remove]");
  if (removeBtn) {
    removeBtn.addEventListener("click", () => item.remove());
  }

  container.appendChild(fragment);
}

function collectSection(section) {
  const container = document.querySelector(`[data-section="${section}"]`);
  if (!container) return [];

  const items = [];
  container.querySelectorAll(".item").forEach((item) => {
    const obj = {};
    item.querySelectorAll("[data-field]").forEach((field) => {
      const key = field.dataset.field;
      obj[key] = (field.value || "").trim();
    });

    const hasValue = Object.values(obj).some((value) => value);
    if (hasValue) items.push(obj);
  });

  return items;
}

function collectMain() {
  const data = {};
  document.querySelectorAll("[data-main]").forEach((field) => {
    const key = field.dataset.main;
    data[key] = (field.value || "").trim();
  });
  return data;
}

function setStatus(message, type = "") {
  const status = document.getElementById("status");
  if (!status) return;
  status.textContent = message;
  status.className = `status ${type}`.trim();
}

function showTemplateSelection(candidateId) {
  const form = document.getElementById("cv-form");
  const mainHeader = document.getElementById("main-header");
  const templateSection = document.getElementById("template-selection");
  const templateHeader = document.getElementById("template-header");

  if (form) form.classList.add("hidden");
  if (mainHeader) mainHeader.classList.add("hidden");

  if (templateSection) templateSection.classList.remove("hidden");
  if (templateHeader) templateHeader.classList.remove("hidden");

  // Attach event listeners to buttons
  document.querySelectorAll("[data-download]").forEach(btn => {
    btn.onclick = () => {
      const style = btn.dataset.download;
      window.open(`/api/download/${candidateId}?style=${style}`, '_blank');
    };
  });

  const backBtn = document.getElementById("back-to-form");
  if (backBtn) {
    backBtn.onclick = () => {
      if (form) form.classList.remove("hidden");
      if (mainHeader) mainHeader.classList.remove("hidden");

      if (templateSection) templateSection.classList.add("hidden");
      if (templateHeader) templateHeader.classList.add("hidden");

      // Go back to the last step (currentStep acts as saved state)
      showStep(currentStep);
      setStatus("");
    };
  }
}

let currentStep = 1;
const totalSteps = 6;

function showStep(step) {
  const form = document.getElementById("cv-form");
  const mainHeader = document.getElementById("main-header");
  const templateSection = document.getElementById("template-selection");
  const templateHeader = document.getElementById("template-header");

  // Step 6 is Template Selection
  if (step === 6) {
    if (form) form.classList.add("hidden");
    if (mainHeader) mainHeader.classList.add("hidden");
    if (templateSection) templateSection.classList.remove("hidden");
    if (templateHeader) templateHeader.classList.remove("hidden");
    return;
  }

  // Steps 1-5: Show Form
  if (form) form.classList.remove("hidden");
  if (mainHeader) mainHeader.classList.remove("hidden");
  if (templateSection) templateSection.classList.add("hidden");
  if (templateHeader) templateHeader.classList.add("hidden");

  document.querySelectorAll(".wizard-step").forEach((el) => {
    el.classList.add("hidden");
    if (parseInt(el.dataset.step) === step) {
      el.classList.remove("hidden");
    }
  });

  const display = document.getElementById("current-step-display");
  if (display) display.textContent = step;

  // Button visibility
  const prevBtn = document.getElementById("prev-step");
  const nextBtn = document.getElementById("next-step");
  const submitBtn = document.getElementById("submit-form");
  const skipBtn = document.getElementById("skip-to-templates");

  if (prevBtn) {
    if (step === 1) prevBtn.classList.add("hidden");
    else prevBtn.classList.remove("hidden");
  }

  if (nextBtn) {
    if (step >= 5) nextBtn.classList.add("hidden"); // Use submit on step 4? No, step 5 is distinct
    else nextBtn.classList.remove("hidden");
  }

  // Step 4 is where we save. Step 5 is search.
  // Wait, if nextBtn is hidden on step 5, how do we search? Search button is separate.
  // How do we go to step 6? Skip button or Apply button.

  if (submitBtn) {
    if (step === 4) submitBtn.classList.remove("hidden");
    else submitBtn.classList.add("hidden");
  }

  if (skipBtn) {
    if (step === 5) skipBtn.classList.remove("hidden");
    else skipBtn.classList.add("hidden");
  }
}

async function searchJobs() {
  const query = document.getElementById("job-query").value;
  const location = document.getElementById("job-location").value;
  const resultsContainer = document.getElementById("job-results");

  resultsContainer.innerHTML = '<p class="text-center">Buscando...</p>';

  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}`);
    const jobs = await res.json();

    resultsContainer.innerHTML = '';

    if (jobs.length === 0) {
      resultsContainer.innerHTML = '<p class="text-center text-muted">No se encontraron ofertas.</p>';
      return;
    }

    jobs.forEach(job => {
      const card = document.createElement('div');
      card.className = 'item';
      card.innerHTML = `
                <div class="item-header">
                    <strong>${job.title}</strong>
                    <span class="text-muted" style="font-size: 0.85rem">${job.company}</span>
                </div>
                <div style="font-size: 0.9rem; margin-bottom: 8px;">
                    ${job.location} | ${new Date(job.date_posted).toLocaleDateString()}
                </div>
                <div class="actions" style="justify-content: flex-end; gap: 8px;">
                    <a href="${job.url}" target="_blank" class="btn ghost" style="font-size: 0.8rem">Ver Original</a>
                    <button class="btn primary small apply-btn" data-url="${job.url}">Aplicar con CV</button>
                </div>
            `;

      // Attach apply listener
      card.querySelector('.apply-btn').addEventListener('click', () => applyJob(job));
      resultsContainer.appendChild(card);
    });

  } catch (e) {
    resultsContainer.innerHTML = `<p class="status error">Error al buscar: ${e.message}</p>`;
  }
}

async function applyJob(job) {
  // Current candidate ID is needed. We should store it globally or in DOM.
  // For now let's assume it's stored in a global variable set on submit.
  if (!window.currentCandidateId) {
    alert("Primero debes guardar tu información (Paso 4).");
    return;
  }

  try {
    const res = await fetch('/api/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        candidate_id: window.currentCandidateId,
        job: job
      })
    });
    const data = await res.json();
    if (data.status === 'success') {
      alert("¡Aplicación registrada! Ahora puedes generar tu CV adaptado.");
      // Ideally navigate to a tailored CV generation or highlight this job
      // For MVP, maybe just download the CV immediately?
      window.open(`/api/download/${window.currentCandidateId}?style=modern`, '_blank');
    }
  } catch (e) {
    alert("Error al aplicar: " + e.message);
  }
}


async function generateSummary() {
  const btn = document.getElementById("btn-generate-summary");
  if (!btn) return;

  const originalText = btn.textContent;
  btn.textContent = "Generando...";
  btn.disabled = true;

  try {
    const data = {
      ...collectMain(),
      experiences: collectSection("experiences"),
      skills: collectSection("skills")
    };

    const res = await fetch("/api/generate_summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();

    const container = document.getElementById("ai-options-container");
    const list = document.getElementById("ai-options-list");
    list.innerHTML = "";

    result.options.forEach((opt) => {
      const div = document.createElement("div");
      div.style.cssText = "padding: 12px; border: 1px solid #ccc; border-radius: 6px; cursor: pointer; background: #fff; margin-bottom: 8px; font-size: 0.9rem; line-height: 1.4;";
      div.textContent = opt;

      div.onmouseover = () => div.style.borderColor = "var(--primary-color)";
      div.onmouseout = () => div.style.borderColor = "#ccc";

      div.onclick = () => {
        document.querySelector('[data-main="summary"]').value = opt;
        container.classList.add("hidden");
      };

      list.appendChild(div);
    });

    container.classList.remove("hidden");

  } catch (e) {
    alert("Error generando perfil: " + e.message);
  } finally {
    btn.textContent = originalText;
    btn.disabled = false;
  }
}

function init() {
  sections.forEach((section) => {
    const addBtn = document.querySelector(`[data-add="${section}"]`);
    if (addBtn) {
      addBtn.addEventListener("click", () => addItem(section));
    }
    addItem(section); // Add initial empty item
  });

  // AI Generator Listeners
  document.getElementById("btn-generate-summary")?.addEventListener("click", generateSummary);
  document.getElementById("close-ai-options")?.addEventListener("click", () => {
    document.getElementById("ai-options-container")?.classList.add("hidden");
  });

  showStep(currentStep);

  document.getElementById("prev-step")?.addEventListener("click", () => {
    if (currentStep > 1) {
      currentStep--;
      showStep(currentStep);
    }
  });

  document.getElementById("next-step")?.addEventListener("click", () => {
    // Validate Step 1
    if (currentStep === 1) {
      const name = document.querySelector('[data-main="full_name"]').value;
      const email = document.querySelector('[data-main="email"]').value;
      if (!name || !email) {
        alert("Por favor completa los campos requeridos (*)");
        return;
      }
    }

    if (currentStep < totalSteps) {
      currentStep++;
      showStep(currentStep);
    }
  });

  document.getElementById("btn-search-jobs")?.addEventListener("click", searchJobs);

  document.getElementById("skip-to-templates")?.addEventListener("click", () => {
    currentStep = 6;
    showStep(currentStep);
  });

  const form = document.getElementById("cv-form");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    setStatus("Guardando...", "info");

    const payload = {
      ...collectMain(),
      experiences: collectSection("experiences"),
      educations: collectSection("educations"),
      skills: collectSection("skills"),
      languages: collectSection("languages"),
      certifications: collectSection("certifications"),
      projects: collectSection("projects"),
      links: collectSection("links"),
    };

    try {
      const response = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        const fields = data.fields ? ` Faltan: ${data.fields.join(", ")}` : "";
        throw new Error(data.error ? `${data.error}.${fields}` : "Error al guardar.");
      }

      const result = await response.json();
      setStatus(`Guardado con ID ${result.candidate_id}.`, "success");

      // Store ID globally for apply function
      window.currentCandidateId = result.candidate_id;

      // Move to Step 5 (Search)
      currentStep = 5;
      showStep(currentStep);

    } catch (error) {
      setStatus(error.message || "Error inesperado.", "error");
    }
  });
}

document.addEventListener("DOMContentLoaded", init);
