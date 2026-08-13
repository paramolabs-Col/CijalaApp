document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const tab = btn.dataset.tab;
    document.getElementById('campaignPage').style.display = tab === 'campaign' ? '' : 'none';
    document.getElementById('ideasPage').style.display = tab === 'ideas' ? '' : 'none';
    document.getElementById('vaultPage').style.display = tab === 'vault' ? '' : 'none';
    if (tab === 'ideas') loadIdeas();
    if (tab === 'vault') loadVault();
  });
});
