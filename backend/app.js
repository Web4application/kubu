document.getElementById('start-btn').addEventListener('click', () => {
  const repoUrl = document.getElementById('repo-url').value.trim();
  const statusMsg = document.getElementById('status-msg');
  const summarySection = document.getElementById('summary');
  const fileListSection = document.getElementById('file-list');
  const upgradeStatusSection = document.getElementById('upgrade-status');

  if (!repoUrl) {
    statusMsg.textContent = 'Please enter a valid GitHub repository URL.';
    return;
  }

  statusMsg.textContent = 'Starting analysis... This might take a while.';
  summarySection.classList.add('hidden');
  fileListSection.classList.add('hidden');
  upgradeStatusSection.classList.add('hidden');

  // Call backend API to start repo analysis
  fetch('/api/start-analysis', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl }),
  })
  .then((res) => {
    if (!res.ok) throw new Error('Failed to start analysis.');
    return res.json();
  })
  .then((data) => {
    statusMsg.textContent = 'Analysis complete! Displaying results...';

    // Display summary
    document.getElementById('project-summary').textContent = data.summary || 'No summary available.';
    summarySection.classList.remove('hidden');

    // Display files & folders
    const filesUl = document.getElementById('files-ul');
    filesUl.innerHTML = '';
    if (data.files && data.files.length) {
      data.files.forEach((file) => {
        const li = document.createElement('li');
        li.textContent = file;
        filesUl.appendChild(li);
      });
      fileListSection.classList.remove('hidden');
    }

    // Display upgrade status
    document.getElementById('upgrade-msg').textContent = data.upgrade_status || 'No upgrade info.';
    upgradeStatusSection.classList.remove('hidden');
  })
  .catch((err) => {
    statusMsg.textContent = 'Error: ' + err.message;
  });
});
