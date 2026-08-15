const ICON_MOON = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>';
const ICON_SUN = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none"><circle cx="12" cy="12" r="4.2" stroke="currentColor" stroke-width="1.7"/><path d="M12 2.5v2.4M12 19.1v2.4M4.9 4.9l1.7 1.7M17.4 17.4l1.7 1.7M2.5 12h2.4M19.1 12h2.4M4.9 19.1l1.7-1.7M17.4 6.6l1.7-1.7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>';

function applyThemeIcon() {
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  const btn = document.getElementById("themeToggle");
  if (btn) btn.innerHTML = isDark ? ICON_SUN : ICON_MOON;
}

applyThemeIcon();

const themeBtn = document.getElementById("themeToggle");
if (themeBtn) {
  themeBtn.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.documentElement.removeAttribute("data-theme");
      try { localStorage.setItem("theme", "light"); } catch (e) {}
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      try { localStorage.setItem("theme", "dark"); } catch (e) {}
    }
    applyThemeIcon();
  });
}
