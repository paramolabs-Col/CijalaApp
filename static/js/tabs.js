function activateTab(tab){
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tab);
  });
  document.getElementById('campaignPage').style.display = tab === 'campaign' ? '' : 'none';
  document.getElementById('templatesPage').style.display = tab === 'templates' ? '' : 'none';
  document.getElementById('ideasPage').style.display = tab === 'ideas' ? '' : 'none';
  document.getElementById('vaultPage').style.display = tab === 'vault' ? '' : 'none';
  if (tab === 'ideas') loadIdeas();
  if (tab === 'vault') loadVault();
  if (tab === 'templates') loadTemplates();
  try { localStorage.setItem('activeTab', tab); } catch (e) {}
}

document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => activateTab(btn.dataset.tab));
});

// Al cargar la página, volver a la última pestaña usada (si hay una guardada)
let savedTab = null;
try { savedTab = localStorage.getItem('activeTab'); } catch (e) {}
if (savedTab && document.querySelector(`.tab-btn[data-tab="${savedTab}"]`)) {
  activateTab(savedTab);
}
