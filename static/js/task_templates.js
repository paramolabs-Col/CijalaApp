let taskTemplates = [];

async function loadTemplates(){
  const res = await fetch("/api/task-templates");
  taskTemplates = await res.json();
  renderTemplates();
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

/* ---------------- Init ---------------- */
loadTemplates();
