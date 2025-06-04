const WebSocket = require('ws');
const { ethers } = require('ethers');

// WebSocket server on port 8080
const wss = new WebSocket.Server({ port: 8080 });

// Connect to Ethereum (or your blockchain) node via WebSocket provider
const provider = new ethers.providers.WebSocketProvider('wss://mainnet.infura.io/ws/v3/YOUR_INFURA_PROJECT_ID');

// Broadcast function to send message to all clients
function broadcast(data) {
  const message = JSON.stringify(data);
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

wss.on('connection', (ws) => {
  console.log('New client connected');

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Listen for new blocks and broadcast block number + timestamp
provider.on('block', async (blockNumber) => {
  const block = await provider.getBlock(blockNumber);
  const data = {
    type: 'block',
    blockNumber,
    timestamp: block.timestamp,
    // Let's do some funky emissive color shifting based on block difficulty & gasUsed
    emissiveR: Math.min(1, block.difficulty / 1e15),
    emissiveG: Math.min(1, block.gasUsed / 1e7),
    emissiveB: 0.5,
  };
  console.log('New block:', data);
  broadcast(data);
});

// Catch errors & reconnect logic (robustness!)
provider._websocket.on('close', () => {
  console.error('WebSocket closed. Reconnecting...');
  setTimeout(() => {
    provider = new ethers.providers.WebSocketProvider('wss://mainnet.infura.io/ws/v3/YOUR_INFURA_PROJECT_ID');
  }, 5000);
});

console.log('Kubu-Hai WebSocket server running on ws://localhost:8080');
