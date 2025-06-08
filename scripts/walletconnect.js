// wallet-connect.js — ethers.js wallet connection logic

(async () => {
  const connectBtn = document.getElementById('connect-wallet-btn');
  const statusText = document.getElementById('wallet-status');

  if (!connectBtn || !statusText) {
    console.warn('Wallet connect elements missing.');
    return;
  }

  if (!window.ethereum) {
    statusText.textContent = 'No Ethereum wallet detected. Please install MetaMask or compatible wallet.';
    connectBtn.disabled = true;
    return;
  }

  let provider;
  try {
    provider = new ethers.BrowserProvider(window.ethereum);
  } catch (err) {
    statusText.textContent = 'Error initializing provider: ' + err.message;
    connectBtn.disabled = true;
    return;
  }

  async function connectWallet() {
    try {
      const accounts = await provider.send('eth_requestAccounts', []);
      if (accounts.length === 0) {
        statusText.textContent = 'No accounts found.';
        return;
      }

      const account = accounts[0];
      const network = await provider.getNetwork();

      statusText.textContent = `Connected: ${account.slice(0,6)}...${account.slice(-4)} on ${network.name}`;
      connectBtn.textContent = 'Disconnect Wallet';

      // Setup disconnect behavior
      connectBtn.onclick = disconnectWallet;
    } catch (err) {
      statusText.textContent = 'Connection rejected or failed.';
    }
  }

  function disconnectWallet() {
    // There’s no standard way to disconnect injected wallets.
    // We'll just reset UI.
    statusText.textContent = 'Wallet disconnected.';
    connectBtn.textContent = 'Connect Wallet';
    connectBtn.onclick = connectWallet;
  }

  // Initial button click binds connect
  connectBtn.onclick = connectWallet;

  // Optional: Detect account/network changes to update status dynamically
  if (window.ethereum.on) {
    window.ethereum.on('accountsChanged', (accounts) => {
      if (accounts.length === 0) {
        disconnectWallet();
      } else {
        connectWallet();
      }
    });

    window.ethereum.on('chainChanged', (_chainId) => {
      // Reload page or update UI on network change
      window.location.reload();
    });
  }
})();
