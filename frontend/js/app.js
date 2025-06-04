const toggleDarkModeBtn = document.getElementById("toggleDarkMode");
const btnCloneRepo = document.getElementById("btnCloneRepo");
const btnAnalyze = document.getElementById("btnAnalyze");
const btnChat = document.getElementById("btnChat");
const btnVoiceChat = document.getElementById("btnVoiceChat");

const cloneSection = document.getElementById("cloneSection");
const chatSection = document.getElementById("chatSection");
const voiceSection = document.getElementById("voiceSection");

const startCloneBtn = document.getElementById("startClone");
const repoUrlInput = document.getElementById("repoUrl");
const cloneStatus = document.getElementById("cloneStatus");

const chatLog = document.getElementById("chatLog");
const chatInput = document.getElementById("chatInput");
const sendChatBtn = document.getElementById("sendChat");

const voiceStatus = document.getElementById("voiceStatus");
const startVoiceChatBtn = document.getElementById("startVoiceChat");

toggleDarkModeBtn.onclick = () => {
  document.body.classList.toggle("dark");
};

btnCloneRepo.onclick = () => {
  cloneSection.classList.remove("hidden");
  chatSection.classList.add("hidden");
  voiceSection.classList.add("hidden");
};

btnChat.onclick = () => {
  cloneSection.classList.add("hidden");
  chatSection.classList.remove("hidden");
  voiceSection.classList.add("hidden");
};

btnVoiceChat.onclick = () => {
  cloneSection.classList.add("hidden");
  chatSection.classList.add("hidden");
  voiceSection.classList.remove("hidden");
};

startCloneBtn.onclick = async () => {
  const url = repoUrlInput.value.trim();
  if (!url) {
    alert("Please enter a GitHub repo URL.");
    return;
  }
  cloneStatus.textContent = "Starting clone and analysis...";
  const response = await fetch("http://localhost:8000/clone-and-analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  const data = await response.json();
  cloneStatus.textContent = data.message;
};

// WebSocket Chat (simple echo example)
let ws;
sendChatBtn.onclick = () => {
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    ws = new WebSocket("ws://localhost:8000/ws");
    ws.onopen = () => {
      ws.send(chatInput.value);
      chatLog.value += `You: ${chatInput.value}\n`;
      chatInput.value = "";
    };
    ws.onmessage = (e) => {
      chatLog.value += `Bot: ${e.data}\n`;
    };
  } else {
    ws.send(chatInput.value);
    chatLog.value += `You: ${chatInput.value}\n`;
    chatInput.value = "";
  }
};

// Voice Chat placeholder
startVoiceChatBtn.onclick = () => {
  voiceStatus.textContent = "Voice chat feature coming soon!";
};
