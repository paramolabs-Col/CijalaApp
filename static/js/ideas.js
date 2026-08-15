let allProjects = [];
let allIdeas = [];

async function loadProjects(){
  const res = await fetch("/api/projects");
  allProjects = await res.json();
  const opts = allProjects.map(p => `<option value="${p.id}">${p.name}</option>`).join("");

  const ideaSelect = document.getElementById("ideaProject");
  ideaSelect.innerHTML = `<option value="">Sin proyecto</option>${opts}<option value="__new__">+ Nuevo proyecto…</option>`;

  const filterSelect = document.getElementById("filterProject");
  filterSelect.innerHTML = `<option value="">Todos los proyectos</option>${opts}`;
}

document.getElementById("ideaProject").addEventListener("change", async (e) => {
  if (e.target.value !== "__new__") return;
  const name = prompt("Nombre del nuevo proyecto:");
  e.target.value = "";
  if (!name || !name.trim()) return;
  const res = await fetch("/api/projects", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name: name.trim()})
  });
  if (res.ok){
    const project = await res.json();
    await loadProjects();
    document.getElementById("ideaProject").value = project.id;
  } else {
    const err = await res.json();
    alert(err.error || "No se pudo crear el proyecto");
  }
});

function projectName(id){
  const p = allProjects.find(p => p.id === id);
  return p ? p.name : id;
}

function renderIdeas(){
  const projectFilter = document.getElementById("filterProject").value;
  const tagFilter = document.getElementById("filterTag").value.trim().toLowerCase();

  const filtered = allIdeas.filter(idea => {
    if (projectFilter && idea.project !== projectFilter) return false;
    if (tagFilter && !idea.tags.some(t => t.toLowerCase().includes(tagFilter))) return false;
    return true;
  });

  const list = document.getElementById("ideasList");
  if (!filtered.length) {
    list.innerHTML = `<div class="empty-state">Sin ideas todavía. Anota la primera arriba.</div>`;
    return;
  }

  list.innerHTML = filtered.map(idea => `
    <div class="idea-card ${idea.done ? 'done' : ''}" data-id="${idea.id}">
      <input type="checkbox" class="idea-done" ${idea.done ? 'checked' : ''}>
      <div class="idea-card-body">
        <div class="idea-text"></div>
        <div class="idea-meta">
          ${idea.project ? `<span class="idea-project">${projectName(idea.project)}</span>` : ''}
          ${idea.tags.map(t => `<span class="idea-tag">#${t}</span>`).join('')}
          <span class="idea-date">${idea.created_at.replace('T', ' ')}</span>
        </div>
      </div>
      <button class="idea-delete" title="Eliminar">✕</button>
    </div>
  `).join('');

  list.querySelectorAll('.idea-card').forEach(card => {
    const idea = filtered.find(i => i.id === card.dataset.id);
    card.querySelector('.idea-text').textContent = idea.text;
  });
}

async function loadIdeas(){
  try{
    const res = await fetch("/api/ideas");
    allIdeas = await res.json();
    renderIdeas();
  }catch(err){
    console.error(err);
  }
}

document.getElementById("ideaForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("ideaText").value.trim();
  if (!text) return;
  const projectVal = document.getElementById("ideaProject").value;
  const project = projectVal === "__new__" ? "" : projectVal;
  const tags = document.getElementById("ideaTags").value;

  await fetch("/api/ideas", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text, project, tags})
  });

  document.getElementById("ideaForm").reset();
  document.getElementById("ideaForm").hidden = true;
  loadIdeas();
});

document.getElementById("ideaCancelBtn").addEventListener("click", () => {
  document.getElementById("ideaForm").hidden = true;
  document.getElementById("ideaForm").reset();
});

document.getElementById("ideasList").addEventListener("click", async (e) => {
  const card = e.target.closest(".idea-card");
  if (!card) return;
  const id = card.dataset.id;

  if (e.target.classList.contains("idea-delete")) {
    if (!confirm("¿Eliminar esta idea?")) return;
    await fetch(`/api/ideas/${id}`, {method: "DELETE"});
    loadIdeas();
  }
});

document.getElementById("ideasList").addEventListener("change", async (e) => {
  if (!e.target.classList.contains("idea-done")) return;
  const card = e.target.closest(".idea-card");
  const id = card.dataset.id;
  await fetch(`/api/ideas/${id}`, {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({done: e.target.checked})
  });
  loadIdeas();
});

document.getElementById("filterProject").addEventListener("change", renderIdeas);
document.getElementById("filterTag").addEventListener("input", renderIdeas);

/* ---------------- Init ---------------- */
loadProjects();
