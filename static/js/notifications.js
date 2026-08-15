const ICON_BELL = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" style="vertical-align:-2px;margin-right:3px;"><path d="M6 10a6 6 0 1 1 12 0c0 3.5 1.2 5 1.8 5.6H4.2C4.8 15 6 13.5 6 10Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M10 19a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>';
const ICON_BELL_OFF = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" style="vertical-align:-2px;margin-right:3px;"><path d="M6 10a6 6 0 0 1 9.6-4.8M18 10c0 3.5 1.2 5 1.8 5.6H4.2M8 15.6H4.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"/><path d="M10 19a2 2 0 0 0 4 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M3 3l18 18" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>';

const NOTIFY_LEAD_MINUTES = 5;
const CHECK_INTERVAL_MS = 60 * 1000;
const notifiedKeys = new Set(); // evita repetir el mismo aviso mientras la app sigue abierta

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/static/sw.js").catch((err) => {
    console.error("No se pudo registrar el service worker:", err);
  });
}

function parseTaskDateTime(dateStr, timeStr) {
  if (!timeStr) return null;
  const m = timeStr.trim().match(/(\d{1,2}):(\d{2})\s*(a\.?\s?m\.?|p\.?\s?m\.?|m\.?)/i);
  if (!m) return null;

  let hour = parseInt(m[1], 10);
  const minute = parseInt(m[2], 10);
  const suffix = m[3].toLowerCase().replace(/[.\s]/g, "");

  if (suffix === "pm" && hour !== 12) hour += 12;
  if (suffix === "am" && hour === 12) hour = 0;
  if (suffix === "m") hour = 12; // "12:00 m." = mediodía

  return new Date(`${dateStr}T${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}:00`);
}

function fireNotification(campaignName, task, dt) {
  const timeLabel = dt.toLocaleTimeString("es-CO", { hour: "2-digit", minute: "2-digit" });
  const options = {
    body: `${task.label} — ${timeLabel} (${campaignName})`,
    icon: "/static/icon-192.png",
    badge: "/static/icon-192.png",
  };

  if (navigator.serviceWorker && navigator.serviceWorker.ready) {
    navigator.serviceWorker.ready.then((reg) => reg.showNotification("Tarea en 5 minutos", options));
  } else if ("Notification" in window) {
    new Notification("Tarea en 5 minutos", options);
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

    campaigns.forEach((campaign) => {
      campaign.days.forEach((day) => {
        day.tasks.forEach((task) => {
          const dt = parseTaskDateTime(day.date, task.time);
          if (!dt) return;

          const diffMin = (dt - now) / 60000;
          const key = `${campaign.id}::${day.date}::${task.id}`;

          if (diffMin > 0 && diffMin <= NOTIFY_LEAD_MINUTES && !state[key] && !notifiedKeys.has(key)) {
            notifiedKeys.add(key);
            fireNotification(campaign.name, task, dt);
          }
        });
      });
    });
  } catch (err) {
    console.error("Error chequeando tareas próximas:", err);
  }
}

function updateNotifyButton(btn) {
  if (!("Notification" in window)) {
    btn.innerHTML = ICON_BELL_OFF + "No disponible en este navegador";
    btn.disabled = true;
    return;
  }
  if (Notification.permission === "granted") {
    btn.innerHTML = ICON_BELL + "Notificaciones activadas";
  } else if (Notification.permission === "denied") {
    btn.innerHTML = ICON_BELL_OFF + "Bloqueadas (habilitalas en ajustes del sitio)";
  } else {
    btn.innerHTML = ICON_BELL + "Activar notificaciones";
  }
}

function initNotifications() {
  const btn = document.getElementById("notifyBtn");
  if (!btn) return;

  updateNotifyButton(btn);

  btn.addEventListener("click", async () => {
    if (!("Notification" in window)) return;
    await Notification.requestPermission();
    updateNotifyButton(btn);
    if (Notification.permission === "granted") {
      checkUpcomingTasks();
    }
  });

  if ("Notification" in window && Notification.permission === "granted") {
    checkUpcomingTasks();
    setInterval(checkUpcomingTasks, CHECK_INTERVAL_MS);
  }
}

initNotifications();
