const TAB_LABELS = {
  campaign:  'Campañas',
  templates: 'Plantillas',
  ideas:     'Ideas',
  todos:     'Tareas',
  vault:     'Baúl',
};

const PAGES = {
  campaign:  document.getElementById('campaignPage'),
  templates: document.getElementById('templatesPage'),
  ideas:     document.getElementById('ideasPage'),
  todos:     document.getElementById('todosPage'),
  vault:     document.getElementById('vaultPage'),
};

function activateTab(tab){
  // Tab buttons (desktop)
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tab);
  });
  // Drawer items (mobile)
  document.querySelectorAll('.drawer-item').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tab);
  });
  // Mobile label
  const lbl = document.getElementById('mobileNavLabel');
  if (lbl) lbl.textContent = TAB_LABELS[tab] || tab;

  // Pages
  Object.keys(PAGES).forEach(key => {
    const el = PAGES[key];
    if (el) el.style.display = key === tab ? 'block' : 'none';
  });

  // Bottom bar sections
  document.querySelectorAll('.bb-section').forEach(s => { s.hidden = true; });
  const bb = document.getElementById('bb-' + tab);
  if (bb) bb.hidden = false;

  // Tab-specific actions
  if (tab === 'ideas')     loadIdeas();
  if (tab === 'vault')     onVaultTabActivated();
  else if (typeof lockVault === 'function') lockVault();
  if (tab === 'templates') loadTemplates();
  if (tab === 'todos')     loadTodos();

  try { localStorage.setItem('activeTab', tab); } catch(e) {}

  // Close drawer if open
  closeDrawer();
}

/* ===== Desktop tab buttons ===== */
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => activateTab(btn.dataset.tab));
});

/* ===== Hamburger / Drawer ===== */
function openDrawer(){
  document.getElementById('navOverlay').hidden = false;
  document.body.style.overflow = 'hidden';
}
function closeDrawer(){
  const overlay = document.getElementById('navOverlay');
  if (overlay) overlay.hidden = true;
  document.body.style.overflow = '';
}

document.getElementById('hamburgerBtn').addEventListener('click', openDrawer);
document.getElementById('hamburgerBtnBar').addEventListener('click', openDrawer);
document.getElementById('navDrawerClose').addEventListener('click', closeDrawer);
document.getElementById('navOverlay').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) closeDrawer();
});
document.querySelectorAll('.drawer-item').forEach(btn => {
  btn.addEventListener('click', () => activateTab(btn.dataset.tab));
});

/* ===== Drawer settings ===== */
document.getElementById('drawerThemeToggle').addEventListener('click', () => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', isDark ? '' : 'dark');
  try { localStorage.setItem('theme', isDark ? 'light' : 'dark'); } catch(e) {}
  closeDrawer();
});

const drawerNotify = document.getElementById('drawerNotifyBtn');
if (drawerNotify){
  drawerNotify.addEventListener('click', () => {
    if (typeof requestNotificationPermission === 'function') requestNotificationPermission();
    else if (Notification && Notification.permission !== 'granted') Notification.requestPermission();
    closeDrawer();
  });
}

/* ===== Ideas form toggle ===== */
document.getElementById('newIdeaBtn').addEventListener('click', () => {
  const form = document.getElementById('ideaForm');
  if (form) {
    form.hidden = false;
    document.getElementById('ideaText').focus();
    form.scrollIntoView({behavior:'smooth', block:'center'});
  }
});

/* ===== Restore last tab ===== */
let savedTab = null;
try { savedTab = localStorage.getItem('activeTab'); } catch(e) {}
if (savedTab && document.querySelector(`.tab-btn[data-tab="${savedTab}"]`)){
  activateTab(savedTab);
}
