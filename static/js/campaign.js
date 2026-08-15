/* ---------------- Icons (generic shapes, not brand logos) ---------------- */
const icons = {
  fb: `<svg viewBox="0 0 24 24" fill="none"><path d="M14 8.5h2.2V5.6h-2.5c-2.3 0-3.7 1.5-3.7 3.9v2H8v3h2v7.5h3.1V14.5h2.3l.4-3h-2.7V9.9c0-.9.3-1.4 1.4-1.4z" fill="currentColor"/></svg>`,
  igfeed: `<svg viewBox="0 0 24 24" fill="none"><rect x="3.5" y="3.5" width="17" height="17" rx="5" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.8"/><circle cx="17" cy="7" r="1" fill="currentColor"/></svg>`,
  igstory: `<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.8" stroke-dasharray="3 3.4"/><circle cx="12" cy="12" r="3.4" fill="currentColor"/></svg>`,
  wa: `<svg viewBox="0 0 24 24" fill="none"><path d="M12 3.5a8.4 8.4 0 0 0-7.2 12.7L4 20.5l4.5-1.2A8.4 8.4 0 1 0 12 3.5Z" stroke="currentColor" stroke-width="1.7"/><path d="M9 10.3c.4 2 2.6 4.2 4.6 4.6.8.2 1.4-.5 1.7-1.1.1-.3 0-.5-.2-.6l-1.5-.8c-.2-.1-.4-.1-.5.1l-.4.6c-.7-.3-1.7-1.2-2-1.9l.6-.5c.1-.1.2-.3.1-.5l-.8-1.6c-.1-.2-.3-.3-.6-.2-.6.2-1.2.7-1 1.9Z" fill="currentColor"/></svg>`,
  wadirect: `<svg viewBox="0 0 24 24" fill="none"><path d="M12 3.5a8.4 8.4 0 0 0-7.2 12.7L4 20.5l4.5-1.2A8.4 8.4 0 1 0 12 3.5Z" stroke="currentColor" stroke-width="1.7"/><path d="M8.5 12h7M8.5 9.5h5M8.5 14.5h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>`
};
const platformLabel = {fb:"Facebook", igfeed:"IG Feed", igstory:"IG Story", wa:"WhatsApp", wadirect:"WhatsApp directo"};
const ICON_EDIT = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" style="vertical-align:-1px;margin-right:3px;"><path d="M4 20l1-4L16 5l3 3L8 19l-4 1Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
const ICON_SAVE = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" style="vertical-align:-1px;margin-right:3px;"><path d="M5 5h11l3 3v11H5V5Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8 5v5h7V5M8 20v-6h8v6" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>';
const platformOrder = ["fb","igfeed","igstory","wa","wadirect"];
const dowNames = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"];
const monthNames = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
const phaseInfo = {}; // ya no se usa para agrupar (ver weekRangeLabel) — queda vacío por compatibilidad

function dateMeta(iso){
  const dt = new Date(iso + "T00:00:00");
  return { dayNum: String(dt.getDate()), dow: dowNames[dt.getDay()], month: monthNames[dt.getMonth()] };
}

function weekRangeLabel(days){
  const first = dateMeta(days[0].date);
  const last = dateMeta(days[days.length - 1].date);
  return first.month === last.month
    ? `${first.dayNum} – ${last.dayNum} de ${last.month}`
    : `${first.dayNum} de ${first.month} – ${last.dayNum} de ${last.month}`;
}

function hexToRgba(hex, alpha){
  const h = hex.replace('#', '');
  const full = h.length === 3 ? h.split('').map(c => c + c).join('') : h;
  const num = parseInt(full, 16);
  const r = (num >> 16) & 255, g = (num >> 8) & 255, b = num & 255;
  return `rgba(${r},${g},${b},${alpha})`;
}

let campaigns = [];
let currentCampaignId = null;
let stateMap = {};
let editingDraft = null; // clon editable de la campaña actual

function currentCampaign(){
  return campaigns.find(c => c.id === currentCampaignId);
}

async function loadCampaigns(preferId){
  const res = await fetch("/api/campaigns");
  campaigns = await res.json();
  if (!campaigns.length) return;

  const select = document.getElementById("campaignSelect");
  select.innerHTML = campaigns.map(c => `<option value="${c.id}" style="color:${c.color||'#0a1f3a'}">● ${c.name}${c.month ? " · " + c.month : ""}</option>`).join("");

  const ncSource = document.getElementById("ncSource");
  ncSource.innerHTML = `<option value="">Vacía (sin días)</option>` +
    campaigns.map(c => `<option value="${c.id}">${c.name}</option>`).join("");

  currentCampaignId = preferId && campaigns.some(c => c.id === preferId) ? preferId : campaigns[0].id;
  select.value = currentCampaignId;
  await loadState();
  renderCampaign();
}

async function loadState(){
  const syncLabel = document.getElementById("syncLabel");
  try{
    const res = await fetch("/api/state");
    stateMap = await res.json();
    syncLabel.textContent = "Progreso sincronizado";
  }catch(err){
    syncLabel.textContent = "Sin conexión al servidor (progreso no guardado)";
  }
}

function taskKey(campaignId, date, taskId){
  return `${campaignId}::${date}::${taskId}`;
}

function renderCampaign(){
  const campaign = currentCampaign();
  const color = campaign.color || '#0a1f3a';
  const main = document.getElementById("main");
  main.innerHTML = "";
  document.getElementById("campTitle").textContent = campaign.name;
  document.getElementById("campSubrange").textContent = campaign.month || "";
  document.getElementById("campEyebrow").textContent = "Plan de publicación";
  document.getElementById("campEyebrow").style.color = color;
  document.getElementById("progressFill").style.background = `linear-gradient(90deg, ${color}, #f5b942)`;

  const dotsContainer = document.getElementById("dayDots");
  dotsContainer.innerHTML = "";

  const sortedDays = campaign.days.slice().sort((a, b) => a.date < b.date ? -1 : 1);
  const showWeeks = sortedDays.length > 7;

  sortedDays.forEach((day, i) => {
    if (showWeeks && i % 7 === 0){
      const weekDays = sortedDays.slice(i, i + 7);
      const weekNum = Math.floor(i / 7) + 1;
      const h = document.createElement("div");
      h.className = "week-heading";
      h.innerHTML = `<span class="num" style="background:${color}">SEMANA ${weekNum}</span><h2>${weekRangeLabel(weekDays)}</h2>`;
      main.appendChild(h);
    }

    const meta = dateMeta(day.date);
    const accent = day.fair ? "#f5b942" : color;
    const card = document.createElement("div");
    card.className = `day${day.fair ? ' fair' : ''}`;
    card.id = `day-${day.date}`;
    card.style.setProperty('--day-color', accent);
    card.style.setProperty('--day-color-soft', hexToRgba(accent, 0.14));

    const head = document.createElement("div");
    head.className = "day-head";
    head.innerHTML = `
      <div class="day-date">
        <div class="day-badge">${meta.dayNum}</div>
        <div>
          <div class="day-name">${meta.dow} ${meta.dayNum} de ${meta.month} ${day.fair ? '<span class="fair-pill">Evento</span>' : ''}</div>
          <div class="day-sub"></div>
        </div>
      </div>
      <div class="day-progress" id="prog-${day.date}"></div>
    `;
    head.querySelector(".day-sub").textContent = day.label;
    card.appendChild(head);

    const tasksWrap = document.createElement("div");
    tasksWrap.className = "tasks";

    day.tasks.forEach((t) => {
      const id = taskKey(campaign.id, day.date, t.id);
      const row = document.createElement("label");
      row.className = "task";
      const platformsHtml = t.platform.map(p => `<span class="platform">${icons[p]||""}${platformLabel[p]||p}</span>`).join("");
      row.innerHTML = `
        <input type="checkbox" data-id="${id}" data-day="${day.date}">
        <div class="task-body">
          <div class="task-top">
            <span class="time-badge"></span>
            ${platformsHtml}
          </div>
          <div class="task-label"></div>
          <div class="task-desc"></div>
        </div>
      `;
      row.querySelector(".time-badge").textContent = t.time;
      row.querySelector(".task-label").textContent = t.label;
      row.querySelector(".task-desc").textContent = t.desc;
      tasksWrap.appendChild(row);
    });

    card.appendChild(tasksWrap);
    main.appendChild(card);

    const dot = document.createElement("div");
    dot.className = `daydot${day.fair ? ' fair' : ''}`;
    dot.style.borderColor = accent;
    if (day.fair) dot.style.background = accent;
    dot.textContent = meta.dayNum;
    dot.title = `${meta.dow} ${meta.dayNum} — ${day.label}`;
    dot.onclick = () => document.getElementById(`day-${day.date}`).scrollIntoView({behavior:"smooth", block:"start"});
    dotsContainer.appendChild(dot);
  });

  applyState();
  updateProgress();
}

function applyState(){
  document.querySelectorAll('#main input[type=checkbox]').forEach(cb => {
    const id = cb.dataset.id;
    if (stateMap[id]){
      cb.checked = true;
      cb.closest(".task").classList.add("done");
    }
  });
}

function updateProgress(){
  const all = document.querySelectorAll('#main input[type=checkbox]');
  let total = all.length, checked = 0;
  all.forEach(cb => { if(cb.checked) checked++; });

  document.getElementById("progressFill").style.width = total ? `${(checked/total)*100}%` : "0%";
  document.getElementById("progressLabel").textContent = `${checked} / ${total} tareas publicadas`;

  const campaign = currentCampaign();
  campaign.days.forEach(day => {
    const dayBoxes = document.querySelectorAll(`input[data-day="${day.date}"]`);
    let c = 0;
    dayBoxes.forEach(cb => { if(cb.checked) c++; });
    const el = document.getElementById(`prog-${day.date}`);
    if(el) el.textContent = `${c}/${dayBoxes.length}`;
  });
}

async function toggleState(id, checked){
  const syncLabel = document.getElementById("syncLabel");
  try{
    await fetch("/api/toggle", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({id, checked})
    });
    stateMap[id] = checked;
    syncLabel.textContent = "Progreso guardado";
  }catch(err){
    syncLabel.textContent = "No se pudo guardar (revisa tu conexión)";
  }
}

document.getElementById("main").addEventListener("change", (e) => {
  if(e.target.matches('input[type=checkbox]')){
    e.target.closest(".task").classList.toggle("done", e.target.checked);
    updateProgress();
    toggleState(e.target.dataset.id, e.target.checked);
  }
});

document.getElementById("resetBtn").addEventListener("click", async () => {
  if(!confirm("¿Borrar el progreso guardado de esta campaña? Esta acción no se puede deshacer.")) return;
  await fetch("/api/reset", {
    method:"POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({campaign_id: currentCampaignId})
  });
  await loadState();
  applyState();
  document.querySelectorAll('#main .task.done').forEach(t => t.classList.remove('done'));
  updateProgress();
});

document.getElementById("campaignSelect").addEventListener("change", (e) => {
  currentCampaignId = e.target.value;
  exitEditMode();
  renderCampaign();
});

/* ---------------- Nueva campaña ---------------- */
document.getElementById("newCampaignBtn").addEventListener("click", () => {
  document.getElementById("newCampaignForm").hidden = false;
  resetRange();
});
document.getElementById("ncCancel").addEventListener("click", () => {
  document.getElementById("newCampaignForm").hidden = true;
});

document.getElementById("newCampaignForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("ncName").value.trim();
  const month = document.getElementById("ncMonth").value.trim();
  const source_id = document.getElementById("ncSource").value;
  const start_date = getRangeStartISO();
  const duration_days = getRangeDurationDays();

  if (!start_date) {
    alert("Elegí al menos el día de inicio en el calendario.");
    return;
  }

  const res = await fetch("/api/campaigns", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, month, source_id, start_date, duration_days})
  });
  const created = await res.json();
  document.getElementById("newCampaignForm").reset();
  document.getElementById("newCampaignForm").hidden = true;
  await loadCampaigns(created.id);
});

document.getElementById("deleteCampaignBtn").addEventListener("click", async () => {
  const campaign = currentCampaign();
  if (!campaign) return;
  if (!confirm(`¿Eliminar la campaña "${campaign.name}"? Esta acción no se puede deshacer.`)) return;
  await fetch(`/api/campaigns/${campaign.id}`, {method: "DELETE"});
  await loadCampaigns();
});

/* ---------------- Editor de campaña ---------------- */
function enterEditMode(){
  editingDraft = JSON.parse(JSON.stringify(currentCampaign()));
  document.getElementById("main").hidden = true;
  document.getElementById("dayDots").hidden = true;
  document.getElementById("campaignEditor").hidden = false;
  document.getElementById("editCampaignBtn").innerHTML = ICON_SAVE + "Guardar cambios";
  document.getElementById("editCampaignBtn").classList.add("primary");
  renderEditor();
}

function exitEditMode(){
  editingDraft = null;
  document.getElementById("main").hidden = false;
  document.getElementById("dayDots").hidden = false;
  document.getElementById("campaignEditor").hidden = true;
  document.getElementById("editCampaignBtn").innerHTML = ICON_EDIT + "Editar";
  document.getElementById("editCampaignBtn").classList.remove("primary");
}

function renderEditor(){
  const wrap = document.getElementById("campaignEditor");
  wrap.innerHTML = "";

  const meta = document.createElement("div");
  meta.className = "panel-form";
  meta.style.maxWidth = "none";
  meta.innerHTML = `
    <label class="field-label">Nombre de la campaña</label>
    <input type="text" id="edName" value="${editingDraft.name.replace(/"/g,'&quot;')}">
    <label class="field-label">Mes / etiqueta</label>
    <input type="text" id="edMonth" value="${(editingDraft.month||'').replace(/"/g,'&quot;')}">
    <label class="field-label">Color de la campaña</label>
    <input type="color" id="edColor" value="${editingDraft.color || '#0a1f3a'}" style="width:60px;height:36px;padding:2px;border-radius:8px;">
  `;
  wrap.appendChild(meta);

  editingDraft.days.slice().sort((a,b)=> a.date < b.date ? -1 : 1).forEach((day) => {
    const idx = editingDraft.days.indexOf(day);
    const dayEl = document.createElement("div");
    dayEl.className = "day-edit";
    dayEl.dataset.idx = idx;

    dayEl.innerHTML = `
      <div class="day-edit-head">
        <input type="date" class="ed-date" value="${day.date}">
        <label><input type="checkbox" class="ed-fair" ${day.fair?'checked':''}> Evento</label>
        <input type="text" class="ed-label" placeholder="Descripción del día" value="${day.label.replace(/"/g,'&quot;')}">
        <button type="button" class="mini-btn danger ed-delday">Eliminar día</button>
      </div>
      <div class="ed-tasks"></div>
      <div class="row" style="align-items:center;">
        <button type="button" class="mini-btn ed-addtask">+ Agregar tarea en blanco</button>
        <select class="ed-picktemplate">
          <option value="">+ Desde plantilla…</option>
          ${taskTemplates.map(t => `<option value="${t.id}">${t.time ? t.time + " — " : ""}${t.label}</option>`).join("")}
        </select>
        <select class="ed-pickdaytemplate">
          <option value="">+ Aplicar combo de día…</option>
          ${dayTemplates.map(dt => `<option value="${dt.id}">${dt.name} (${dt.tasks.length})</option>`).join("")}
        </select>
      </div>
    `;

    const tasksBox = dayEl.querySelector(".ed-tasks");
    day.tasks.forEach((task, ti) => {
      tasksBox.appendChild(buildTaskEditRow(task, idx, ti));
    });

    wrap.appendChild(dayEl);
  });

  const addDayBtn = document.createElement("button");
  addDayBtn.type = "button";
  addDayBtn.className = "toolbar-btn";
  addDayBtn.textContent = "+ Agregar día";
  addDayBtn.onclick = () => {
    editingDraft.days.push({date: new Date().toISOString().slice(0,10), phase: 1, fair: false, label: "Nuevo día", tasks: []});
    renderEditor();
  };
  wrap.appendChild(addDayBtn);

  wrap.querySelectorAll(".ed-date").forEach(inp => inp.addEventListener("change", (e) => {
    editingDraft.days[e.target.closest(".day-edit").dataset.idx].date = e.target.value;
  }));
  wrap.querySelectorAll(".ed-fair").forEach(inp => inp.addEventListener("change", (e) => {
    editingDraft.days[e.target.closest(".day-edit").dataset.idx].fair = e.target.checked;
  }));
  wrap.querySelectorAll(".ed-label").forEach(inp => inp.addEventListener("input", (e) => {
    editingDraft.days[e.target.closest(".day-edit").dataset.idx].label = e.target.value;
  }));
  wrap.querySelectorAll(".ed-delday").forEach(btn => btn.addEventListener("click", (e) => {
    const idx = e.target.closest(".day-edit").dataset.idx;
    editingDraft.days.splice(idx, 1);
    renderEditor();
  }));
  wrap.querySelectorAll(".ed-addtask").forEach(btn => btn.addEventListener("click", (e) => {
    const idx = e.target.closest(".day-edit").dataset.idx;
    editingDraft.days[idx].tasks.push({id: null, time:"", platform:[], label:"", desc:""});
    renderEditor();
  }));
  wrap.querySelectorAll(".ed-picktemplate").forEach(sel => sel.addEventListener("change", (e) => {
    const templateId = e.target.value;
    if (!templateId) return;
    const idx = e.target.closest(".day-edit").dataset.idx;
    const tpl = taskTemplates.find(t => t.id === templateId);
    if (!tpl) return;
    editingDraft.days[idx].tasks.push({
      id: null, time: tpl.time, platform: [...tpl.platform], label: tpl.label, desc: tpl.desc
    });
    renderEditor();
  }));
  wrap.querySelectorAll(".ed-pickdaytemplate").forEach(sel => sel.addEventListener("change", (e) => {
    const dtId = e.target.value;
    if (!dtId) return;
    const idx = e.target.closest(".day-edit").dataset.idx;
    const dayTpl = dayTemplates.find(d => d.id === dtId);
    if (!dayTpl) return;
    dayTpl.tasks.forEach(t => {
      editingDraft.days[idx].tasks.push({
        id: null, time: t.time, platform: [...t.platform], label: t.label, desc: t.desc
      });
    });
    renderEditor();
  }));
}

function buildTaskEditRow(task, dayIdx, taskIdx){
  const row = document.createElement("div");
  row.className = "task-edit";
  row.dataset.dayIdx = dayIdx;
  row.dataset.taskIdx = taskIdx;

  const platformChecks = platformOrder.map(p => `
    <label><input type="checkbox" class="ed-platform" value="${p}" ${task.platform.includes(p)?'checked':''}> ${platformLabel[p]}</label>
  `).join("");

  row.innerHTML = `
    <div class="row">
      <input type="text" class="ed-time" placeholder="Hora (ej: 9:00 a.m.)" value="${(task.time||'').replace(/"/g,'&quot;')}" style="max-width:160px;">
      <button type="button" class="mini-btn danger ed-deltask" style="margin-left:auto;">Eliminar tarea</button>
    </div>
    <div class="platform-checks">${platformChecks}</div>
    <input type="text" class="ed-tlabel" placeholder="Título de la tarea" value="${(task.label||'').replace(/"/g,'&quot;')}">
    <textarea class="ed-tdesc" placeholder="Descripción" style="min-height:44px;">${task.desc||''}</textarea>
  `;

  row.querySelector(".ed-time").addEventListener("input", (e) => {
    editingDraft.days[dayIdx].tasks[taskIdx].time = e.target.value;
  });
  row.querySelector(".ed-tlabel").addEventListener("input", (e) => {
    editingDraft.days[dayIdx].tasks[taskIdx].label = e.target.value;
  });
  row.querySelector(".ed-tdesc").addEventListener("input", (e) => {
    editingDraft.days[dayIdx].tasks[taskIdx].desc = e.target.value;
  });
  row.querySelectorAll(".ed-platform").forEach(cb => cb.addEventListener("change", () => {
    const checked = [...row.querySelectorAll(".ed-platform:checked")].map(c => c.value);
    editingDraft.days[dayIdx].tasks[taskIdx].platform = checked;
  }));
  row.querySelector(".ed-deltask").addEventListener("click", () => {
    editingDraft.days[dayIdx].tasks.splice(taskIdx, 1);
    renderEditor();
  });

  return row;
}

document.getElementById("editCampaignBtn").addEventListener("click", async () => {
  if (!editingDraft){
    enterEditMode();
    return;
  }
  editingDraft.name = document.getElementById("edName").value.trim() || editingDraft.name;
  editingDraft.month = document.getElementById("edMonth").value.trim();
  editingDraft.color = document.getElementById("edColor").value;

  const res = await fetch(`/api/campaigns/${editingDraft.id}`, {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name: editingDraft.name, month: editingDraft.month, color: editingDraft.color, days: editingDraft.days})
  });
  await res.json();
  exitEditMode();
  await loadCampaigns(editingDraft.id);
});

/* ---------------- Init ---------------- */
loadCampaigns();
