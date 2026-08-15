const ICON_BELL = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" style="vertical-align:-2px;margin-right:3px;"><path d="M6 10a6 6 0 1 1 12 0c0 3.5 1.2 5 1.8 5.6H4.2C4.8 15 6 13.5 6 10Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M10 19a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>';
const ICON_BELL_OFF = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" style="vertical-align:-2px;margin-right:3px;"><path d="M6 10a6 6 0 0 1 9.6-4.8M18 10c0 3.5 1.2 5 1.8 5.6H4.2M8 15.6H4.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"/><path d="M10 19a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M3 3l18 18" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>';

const CHECK_INTERVAL_MS = 60 * 1000;
const notifiedKeys = new Set();

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/static/sw.js").catch(() => {});
}

/* Entiende tanto "9:00 a.m." como "09:00" (HH:MM del time picker) */
function parseTaskDateTime(dateStr, timeStr) {
  if (!timeStr) return null;

  // Formato HH:MM (24h, guardado por <input type="time">)
  const hm = timeStr.trim().match(/^(\d{1,2}):(\d{2})$/);
  if (hm) {
    return new Date(`${dateStr}T${String(parseInt(hm[1])).padStart(2,'0')}:${hm[2]}:00`);
  }

  // Formato legado "9:00 a.m." / "3:30 p.m." / "12:00 m."
  const m = timeStr.trim().match(/(\d{1,2}):(\d{2})\s*(a\.?\s?m\.?|p\.?\s?m\.?|m\.?)/i);
  if (!m) return null;
  let hour = parseInt(m[1], 10);
  const minute = parseInt(m[2], 10);
  const suffix = m[3].toLowerCase().replace(/[.\s]/g, "");
  if (suffix === "pm" && hour !== 12) hour += 12;
  if (suffix === "am" && hour === 12) hour = 0;
  if (suffix === "m") hour = 12;
  return new Date(`${dateStr}T${String(hour).padStart(2,"0")}:${String(minute).padStart(2,"0")}:00`);
}

function fireNotification(title, body) {
  const options = { body, icon: "/static/icon-192.png", badge: "/static/icon-192.png" };
  if (navigator.serviceWorker && navigator.serviceWorker.ready) {
    navigator.serviceWorker.ready.then(reg => reg.showNotification(title, options));
  } else if ("Notification" in window) {
    new Notification(title, options);
  }
}

async function checkUpcomingTasks() {
  if (!("Notification" in window) || Notification.permission !== "granted") return;
  try {
    const [campaignsRes, stateRes] = await Promise.all([
      fetch("/api/campaigns"),
      fetch("/api/state"),
    ]);
    const campaigns = await campaignsRes.json();
    const state = await stateRes.json();
    const now = new Date();

    campaigns.forEach(campaign => {
      campaign.days.forEach(day => {
        day.tasks.forEach(task => {
          const dt = parseTaskDateTime(day.date, task.time);
          if (!dt) return;
          const diffMin = (dt - now) / 60000;
          const key = `${campaign.id}::${day.date}::${task.id}`;
          if (notifiedKeys.has(key) || state[key]) return;

          if (diffMin >= 0 && diffMin < 1) {
            // Hora exacta
            notifiedKeys.add(key);
            fireNotification("⏰ Hora de publicar", `${task.label} — ${campaign.name}`);
          } else if (diffMin >= 1 && diffMin <= 6) {
            // 5 minutos antes
            const warnKey = key + '::warn';
            if (!notifiedKeys.has(warnKey)) {
              notifiedKeys.add(warnKey);
              fireNotification("🔔 En 5 minutos", `${task.label} — ${campaign.name}`);
            }
          }
        });
      });
    });
  } catch (err) {
    console.error("Error chequeando tareas:", err);
  }
}

function updateNotifyButton(btn) {
  if (!("Notification" in window)) {
    btn.innerHTML = ICON_BELL_OFF + "No disponible";
    btn.disabled = true;
    return;
  }
  if (Notification.permission === "granted") {
    btn.innerHTML = ICON_BELL + "Notificaciones activadas ✓";
  } else if (Notification.permission === "denied") {
    btn.innerHTML = ICON_BELL_OFF + "Bloqueadas — habilitá en ajustes del sitio";
  } else {
    btn.innerHTML = ICON_BELL + "Activar notificaciones";
  }
}

function requestNotificationPermission() {
  if (!("Notification" in window)) return;
  Notification.requestPermission().then(() => {
    const btn = document.getElementById("notifyBtn");
    if (btn) updateNotifyButton(btn);
    const drawerBtn = document.getElementById("drawerNotifyBtn");
    if (drawerBtn) updateDrawerNotifyLabel();
    if (Notification.permission === "granted") startNotificationLoop();
  });
}

function updateDrawerNotifyLabel() {
  const btn = document.getElementById("drawerNotifyBtn");
  if (!btn) return;
  const granted = "Notification" in window && Notification.permission === "granted";
  btn.querySelector('svg + span, span') && (btn.childNodes[btn.childNodes.length-1].textContent = granted ? "Notificaciones activadas ✓" : "Notificaciones");
}

let notifLoopStarted = false;
function startNotificationLoop() {
  if (notifLoopStarted) return;
  notifLoopStarted = true;
  checkUpcomingTasks();
  setInterval(checkUpcomingTasks, CHECK_INTERVAL_MS);
}

/* Arrancar automáticamente si ya hay permiso */
if ("Notification" in window && Notification.permission === "granted") {
  startNotificationLoop();
}

/* Botón legacy (si existe) */
const notifyBtnLegacy = document.getElementById("notifyBtn");
if (notifyBtnLegacy) {
  updateNotifyButton(notifyBtnLegacy);
  notifyBtnLegacy.addEventListener("click", requestNotificationPermission);
}
