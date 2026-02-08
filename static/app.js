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

function init() {
  sections.forEach((section) => {
    const addBtn = document.querySelector(`[data-add="${section}"]`);
    if (addBtn) {
      addBtn.addEventListener("click", () => addItem(section));
    }
    addItem(section);
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
      form.reset();
      sections.forEach((section) => {
        const container = document.querySelector(`[data-section="${section}"]`);
        if (!container) return;
        container.innerHTML = "";
        addItem(section);
      });
    } catch (error) {
      setStatus(error.message || "Error inesperado.", "error");
    }
  });
}

document.addEventListener("DOMContentLoaded", init);
