let taskTemplates = [];
let dayTemplates = [];

async function loadTemplates(){
  const res = await fetch("/api/task-templates");
  taskTemplates = await res.json();
  renderTemplates();
  renderDayTemplateChecklist();
  if (typeof refreshTemplatePicker === "function") refreshTemplatePicker();
}

function renderTemplates(){
  const list = document.getElementById("templatesList");
  if (!taskTemplates.length){
    list.innerHTML = `<div class="empty-state">Sin plantillas todavía. Creá la primera arriba.</div>`;
    return;
  }

  list.innerHTML = taskTemplates.map(tpl => `
    <div class="template-card" data-id="${tpl.id}">
      <div class="template-card-body">
        <div class="template-top">
          <span class="time-badge"></span>
          ${tpl.platform.map(p => `<span class="platform">${icons[p]||""}${platformLabel[p]||p}</span>`).join('')}
        </div>
        <div class="template-label"></div>
        <div class="template-desc"></div>
      </div>
      <div class="template-actions">
        <button type="button" class="mini-btn tpl-delete">Eliminar</button>
      </div>
    </div>
  `).join('');

  list.querySelectorAll(".template-card").forEach(card => {
    const tpl = taskTemplates.find(t => t.id === card.dataset.id);
    card.querySelector(".time-badge").textContent = tpl.time;
    card.querySelector(".template-label").textContent = tpl.label;
    card.querySelector(".template-desc").textContent = tpl.desc;
  });
}

document.getElementById("templateForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const time = document.getElementById("tplTime").value.trim();
  const label = document.getElementById("tplLabel").value.trim();
  const desc = document.getElementById("tplDesc").value.trim();
  const platform = [...document.querySelectorAll('#tplPlatforms input:checked')].map(c => c.value);

  if (!label) return;

  await fetch("/api/task-templates", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({time, label, desc, platform})
  });

  document.getElementById("templateForm").reset();
  loadTemplates();
});

document.getElementById("templatesList").addEventListener("click", async (e) => {
  if (!e.target.classList.contains("tpl-delete")) return;
  const card = e.target.closest(".template-card");
  const id = card.dataset.id;
  const tpl = taskTemplates.find(t => t.id === id);
  if (!confirm(`¿Eliminar la plantilla "${tpl.label}"?`)) return;
  await fetch(`/api/task-templates/${id}`, {method: "DELETE"});
  loadTemplates();
});

/* ==================================================================
   PLANTILLAS DE DÍA (combos de varias tareas)
   ================================================================== */
function renderDayTemplateChecklist(){
  const box = document.getElementById("dtTaskChecklist");
  if (!taskTemplates.length){
    box.innerHTML = `<div class="dt-empty">Creá primero alguna plantilla de tarea arriba.</div>`;
    return;
  }
  box.innerHTML = taskTemplates.map(t => `
    <label><input type="checkbox" value="${t.id}"> ${t.time ? t.time + " — " : ""}${t.label}</label>
  `).join("");
}

async function loadDayTemplates(){
  const res = await fetch("/api/day-templates");
  dayTemplates = await res.json();
  renderDayTemplatesList();
  if (typeof refreshDayTemplatePicker === "function") refreshDayTemplatePicker();
}

function renderDayTemplatesList(){
  const list = document.getElementById("dayTemplatesList");
  if (!dayTemplates.length){
    list.innerHTML = `<div class="empty-state">Sin combos todavía.</div>`;
    return;
  }

  list.innerHTML = dayTemplates.map(dt => `
    <div class="day-template-card" data-id="${dt.id}">
      <div class="day-template-body">
        <div class="day-template-name"></div>
        <div class="day-template-tasks"></div>
      </div>
      <button type="button" class="mini-btn danger dt-delete">Eliminar</button>
    </div>
  `).join("");

  list.querySelectorAll(".day-template-card").forEach(card => {
    const dt = dayTemplates.find(d => d.id === card.dataset.id);
    card.querySelector(".day-template-name").textContent = `${dt.name} (${dt.tasks.length} tareas)`;
    card.querySelector(".day-template-tasks").textContent =
      dt.tasks.map(t => `${t.time ? t.time + " " : ""}${t.label}`).join(" · ");
  });
}

document.getElementById("dayTemplateForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("dtName").value.trim();
  const checkedIds = [...document.querySelectorAll('#dtTaskChecklist input:checked')].map(c => c.value);
  if (!name || !checkedIds.length) return;

  const tasks = checkedIds
    .map(id => taskTemplates.find(t => t.id === id))
    .filter(Boolean)
    .map(t => ({time: t.time, platform: t.platform, label: t.label, desc: t.desc}));

  const res = await fetch("/api/day-templates", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, tasks})
  });
  if (res.ok){
    document.getElementById("dayTemplateForm").reset();
    loadDayTemplates();
  } else {
    const err = await res.json();
    alert(err.error || "No se pudo guardar el combo");
  }
});

document.getElementById("dayTemplatesList").addEventListener("click", async (e) => {
  if (!e.target.classList.contains("dt-delete")) return;
  const card = e.target.closest(".day-template-card");
  const id = card.dataset.id;
  const dt = dayTemplates.find(d => d.id === id);
  if (!confirm(`¿Eliminar el combo "${dt.name}"?`)) return;
  await fetch(`/api/day-templates/${id}`, {method: "DELETE"});
  loadDayTemplates();
});

/* ---------------- Init ---------------- */
loadTemplates();
loadDayTemplates();
