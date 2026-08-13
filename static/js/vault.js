let vaultEntries = [];
const revealedPasswords = {};

async function loadVault(){
  const res = await fetch("/api/vault");
  vaultEntries = await res.json();
  renderVault();
}

function renderVault(){
  const list = document.getElementById("vaultList");
  if (!vaultEntries.length){
    list.innerHTML = `<div class="empty-state">Sin contraseñas guardadas todavía.</div>`;
    return;
  }

  list.innerHTML = vaultEntries.map(entry => `
    <div class="vault-card" data-id="${entry.id}">
      <div class="vault-card-top">
        <div class="vault-name"></div>
      </div>
      ${entry.username ? `<div class="vault-field">👤 <span class="val user-val"></span></div>` : ''}
      <div class="vault-field">🔑 <span class="val pw-val">••••••••</span>
        <button type="button" class="mini-btn v-reveal">Mostrar</button>
        <button type="button" class="mini-btn v-copy">Copiar</button>
      </div>
      ${entry.url ? `<div class="vault-field">🔗 <a class="url-val" target="_blank" rel="noopener"></a></div>` : ''}
      ${entry.notes ? `<div class="vault-field notes-val" style="white-space:pre-wrap;"></div>` : ''}
      <div class="vault-actions">
        <button type="button" class="mini-btn v-edit">Editar</button>
        <button type="button" class="mini-btn danger v-delete">Eliminar</button>
      </div>
    </div>
  `).join('');

  list.querySelectorAll(".vault-card").forEach(card => {
    const entry = vaultEntries.find(e => e.id === card.dataset.id);
    card.querySelector(".vault-name").textContent = entry.name;
    const userEl = card.querySelector(".user-val");
    if (userEl) userEl.textContent = entry.username;
    const urlEl = card.querySelector(".url-val");
    if (urlEl){ urlEl.textContent = entry.url; urlEl.href = entry.url; }
    const notesEl = card.querySelector(".notes-val");
    if (notesEl) notesEl.textContent = entry.notes;
  });
}

document.getElementById("vaultForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    name: document.getElementById("vName").value.trim(),
    username: document.getElementById("vUsername").value.trim(),
    password: document.getElementById("vPassword").value,
    url: document.getElementById("vUrl").value.trim(),
    notes: document.getElementById("vNotes").value.trim(),
  };
  const res = await fetch("/api/vault", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  if (res.ok){
    document.getElementById("vaultForm").reset();
    loadVault();
  } else {
    const err = await res.json();
    alert(err.error || "No se pudo guardar");
  }
});

document.getElementById("vaultList").addEventListener("click", async (e) => {
  const card = e.target.closest(".vault-card");
  if (!card) return;
  const id = card.dataset.id;
  const entry = vaultEntries.find(x => x.id === id);

  if (e.target.classList.contains("v-reveal")){
    const pwEl = card.querySelector(".pw-val");
    if (revealedPasswords[id]){
      pwEl.textContent = "••••••••";
      delete revealedPasswords[id];
      e.target.textContent = "Mostrar";
    } else {
      const res = await fetch(`/api/vault/${id}/reveal`);
      const data = await res.json();
      revealedPasswords[id] = data.password;
      pwEl.textContent = data.password;
      e.target.textContent = "Ocultar";
    }
  }

  if (e.target.classList.contains("v-copy")){
    let pw = revealedPasswords[id];
    if (!pw){
      const res = await fetch(`/api/vault/${id}/reveal`);
      const data = await res.json();
      pw = data.password;
    }
    try{
      await navigator.clipboard.writeText(pw);
      e.target.textContent = "¡Copiado!";
      setTimeout(() => { e.target.textContent = "Copiar"; }, 1500);
    }catch(err){
      alert("No se pudo copiar automáticamente. Contraseña: " + pw);
    }
  }

  if (e.target.classList.contains("v-delete")){
    if (!confirm(`¿Eliminar "${entry.name}" del baúl?`)) return;
    await fetch(`/api/vault/${id}`, {method: "DELETE"});
    loadVault();
  }

  if (e.target.classList.contains("v-edit")){
    const newName = prompt("Nombre:", entry.name);
    if (newName === null) return;
    const newUsername = prompt("Usuario / email:", entry.username || "");
    const newUrl = prompt("URL:", entry.url || "");
    const newNotes = prompt("Notas:", entry.notes || "");
    const newPassword = prompt("Nueva contraseña (déjalo vacío para no cambiarla):", "");

    await fetch(`/api/vault/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: newName, username: newUsername, url: newUrl, notes: newNotes,
        password: newPassword || undefined
      })
    });
    loadVault();
  }
});
