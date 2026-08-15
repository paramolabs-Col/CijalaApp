/* ---------------- PIN del Baúl ---------------- */
const PIN_KEY = 'vault_pin_hash';
let vaultUnlocked = false;
let pinBuffer = '';
let pinState = 'unlock'; // 'unlock' | 'create' | 'confirm'
let pinFirst  = '';
let pinListenersAttached = false;

function simpleHash(str){
  let h = 0;
  for (let i = 0; i < str.length; i++) h = (Math.imul(31, h) + str.charCodeAt(i)) | 0;
  return String(h);
}

function getSavedPin(){ try { return localStorage.getItem(PIN_KEY); } catch(e){ return null; } }
function savePin(pin){ try { localStorage.setItem(PIN_KEY, simpleHash(pin)); } catch(e){} }
function clearSavedPin(){ try { localStorage.removeItem(PIN_KEY); } catch(e){} }

function setPinUI(title, sub, showReset){
  document.getElementById('vaultPinTitle').textContent = title;
  document.getElementById('vaultPinSub').textContent   = sub;
  document.getElementById('vaultResetPin').hidden = !showReset;
}

function updatePinDots(){
  document.querySelectorAll('#vaultPinDots span').forEach((s, i) => {
    s.classList.toggle('filled', i < pinBuffer.length);
  });
}

function pinError(msg){
  const el = document.getElementById('vaultPinError');
  el.textContent = msg; el.hidden = false;
  el.style.animation = 'none';
  requestAnimationFrame(() => { el.style.animation = 'shake .3s ease'; });
  setTimeout(() => { el.hidden = true; }, 2500);
}

function unlockVault(){
  vaultUnlocked = true;
  pinBuffer = '';
  document.getElementById('vaultPinScreen').hidden = true;
  document.getElementById('vaultContent').hidden = false;
  loadVault();
}

function lockVault(){
  vaultUnlocked = false;
  pinBuffer = ''; pinFirst = '';
  pinState = getSavedPin() ? 'unlock' : 'create';
  updatePinDots();
  document.getElementById('vaultPinScreen').hidden = false;
  document.getElementById('vaultContent').hidden = true;
  document.getElementById('vaultPinError').hidden = true;
  if (pinState === 'unlock'){
    setPinUI('Ingresá tu PIN de 4 dígitos', 'El baúl está protegido. Ingresá el PIN para continuar.', true);
  } else {
    setPinUI('Creá tu PIN de 4 dígitos', 'Elegí un PIN para proteger el baúl.', false);
  }
}

function handlePinOK(){
  if (pinBuffer.length < 4){ pinError('Ingresá los 4 dígitos'); return; }

  if (pinState === 'unlock'){
    if (simpleHash(pinBuffer) === getSavedPin()){
      unlockVault();
    } else {
      pinBuffer = ''; updatePinDots(); pinError('PIN incorrecto. Intentá de nuevo.');
    }

  } else if (pinState === 'create'){
    pinFirst = pinBuffer;
    pinBuffer = '';
    pinState = 'confirm';
    updatePinDots();
    setPinUI('Confirmá tu PIN', 'Ingresá el mismo PIN para confirmar.', false);

  } else if (pinState === 'confirm'){
    if (pinBuffer === pinFirst){
      savePin(pinBuffer);
      unlockVault();
    } else {
      pinBuffer = ''; pinFirst = ''; pinState = 'create';
      updatePinDots();
      pinError('Los PINs no coinciden. Empezá de nuevo.');
      setPinUI('Creá tu PIN de 4 dígitos', 'Elegí un PIN para proteger el baúl.', false);
    }
  }
}

function attachPinListeners(){
  if (pinListenersAttached) return;
  pinListenersAttached = true;

  document.querySelectorAll('.pin-key').forEach(btn => {
    btn.addEventListener('click', () => {
      const k = btn.dataset.k;
      if      (k === 'C' )  { pinBuffer = pinBuffer.slice(0, -1); }
      else if (k === 'OK')  { handlePinOK(); return; }
      else if (pinBuffer.length < 4){ pinBuffer += k; }
      updatePinDots();
    });
  });

  document.getElementById('vaultResetPin').addEventListener('click', () => {
    if (!confirm('¿Borrar el PIN guardado? Tendrás que crear uno nuevo.')) return;
    clearSavedPin();
    pinBuffer = ''; pinFirst = ''; pinState = 'create';
    updatePinDots();
    setPinUI('Creá tu PIN de 4 dígitos', 'Elegí un PIN para proteger el baúl.', false);
  });
}

/* Se llama desde tabs.js cuando se activa el tab vault */
function onVaultTabActivated(){
  lockVault();
  attachPinListeners();
}

/* ---------------- Vault data ---------------- */
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
