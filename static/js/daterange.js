const dowNamesShort = ["DO", "LU", "MA", "MI", "JU", "VI", "SA"];
const monthNamesCap = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];

let rangeViewDate = new Date();
let rangeStart = null;
let rangeEnd = null;

function pad2(n){ return String(n).padStart(2, "0"); }
function toISODate(d){ return `${d.getFullYear()}-${pad2(d.getMonth()+1)}-${pad2(d.getDate())}`; }
function isSameDay(a, b){
  return a && b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}
function formatShortDate(d){
  return `${d.getDate()} de ${monthNamesCap[d.getMonth()].toLowerCase()}`;
}

function getRangeStartISO(){
  return rangeStart ? toISODate(rangeStart) : "";
}
function getRangeDurationDays(){
  if (rangeStart && rangeEnd) return Math.round((rangeEnd - rangeStart) / 86400000) + 1;
  if (rangeStart) return 1;
  return 0;
}
function resetRange(){
  rangeStart = null;
  rangeEnd = null;
  rangeViewDate = new Date();
  renderCalendar();
  updateRangeSummary();
}

function updateRangeSummary(){
  const el = document.getElementById("ncRangeSummary");
  if (!el) return;
  if (rangeStart && rangeEnd){
    const days = getRangeDurationDays();
    el.textContent = `${formatShortDate(rangeStart)} al ${formatShortDate(rangeEnd)} (${days} día${days === 1 ? "" : "s"})`;
  } else if (rangeStart){
    el.textContent = `Inicio: ${formatShortDate(rangeStart)} — elegí el día final`;
  } else {
    el.textContent = "Elegí el día de inicio y el día final";
  }
}

function renderCalendar(){
  const container = document.getElementById("ncCalendar");
  if (!container) return;

  const year = rangeViewDate.getFullYear();
  const month = rangeViewDate.getMonth();
  const firstOfMonth = new Date(year, month, 1);
  const startDow = firstOfMonth.getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const daysInPrevMonth = new Date(year, month, 0).getDate();

  const cells = [];
  for (let i = startDow - 1; i >= 0; i--){
    cells.push(new Date(year, month - 1, daysInPrevMonth - i));
  }
  for (let d = 1; d <= daysInMonth; d++){
    cells.push(new Date(year, month, d));
  }
  let nextDay = 1;
  while (cells.length < 42){
    cells.push(new Date(year, month + 1, nextDay));
    nextDay++;
  }

  const monthLabel = `${monthNamesCap[month]} de ${year}`;
  const today = new Date();

  let html = `
    <div class="cal-header">
      <button type="button" class="cal-nav" id="calPrev">‹</button>
      <span class="cal-month">${monthLabel}</span>
      <button type="button" class="cal-nav" id="calNext">›</button>
    </div>
    <div class="cal-grid cal-dow">${dowNamesShort.map(d => `<span>${d}</span>`).join("")}</div>
    <div class="cal-grid cal-days">
  `;

  cells.forEach(date => {
    const muted = date.getMonth() !== month;
    const isStart = rangeStart && isSameDay(date, rangeStart);
    const isEnd = rangeEnd && isSameDay(date, rangeEnd);
    const inRange = rangeStart && rangeEnd && date > rangeStart && date < rangeEnd;

    let cls = "cal-day";
    if (muted) cls += " muted";
    if (isStart || isEnd) cls += " selected";
    if (inRange) cls += " in-range";
    if (isSameDay(date, today)) cls += " today";

    html += `<button type="button" class="${cls}" data-date="${toISODate(date)}">${date.getDate()}</button>`;
  });

  html += `</div>
    <div class="cal-actions">
      <button type="button" class="cal-link" id="calClear">Borrar</button>
      <button type="button" class="cal-link" id="calToday">Hoy</button>
    </div>
  `;

  container.innerHTML = html;

  document.getElementById("calPrev").addEventListener("click", () => {
    rangeViewDate = new Date(rangeViewDate.getFullYear(), rangeViewDate.getMonth() - 1, 1);
    renderCalendar();
  });
  document.getElementById("calNext").addEventListener("click", () => {
    rangeViewDate = new Date(rangeViewDate.getFullYear(), rangeViewDate.getMonth() + 1, 1);
    renderCalendar();
  });
  document.getElementById("calClear").addEventListener("click", () => {
    rangeStart = null;
    rangeEnd = null;
    renderCalendar();
    updateRangeSummary();
  });
  document.getElementById("calToday").addEventListener("click", () => {
    rangeViewDate = new Date();
    renderCalendar();
  });

  container.querySelectorAll(".cal-day").forEach(btn => {
    btn.addEventListener("click", () => {
      const d = new Date(btn.dataset.date + "T00:00:00");
      if (!rangeStart || (rangeStart && rangeEnd)){
        rangeStart = d;
        rangeEnd = null;
      } else if (d < rangeStart){
        rangeEnd = rangeStart;
        rangeStart = d;
      } else {
        rangeEnd = d;
      }
      renderCalendar();
      updateRangeSummary();
    });
  });
}

renderCalendar();
updateRangeSummary();
