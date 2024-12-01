const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const { Client, GatewayIntentBits } = require('discord.js');

const app = express();
const port = 3000;

app.use(bodyParser.json());

// Discord bot setup
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const discordToken = '1156354267817447486';
const openaiApiKey = 'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10';

client.once('ready', () => {
console.log('Discord bot is online!');
});

client.on('messageCreate', async message => {
if (message.author.bot) return;

if (message.content.startsWith('!analyze')) {
const text = message.content.slice(9).trim();
if (!text) {
return message.channel.send('Please provide some text to analyze.');
}

try {
const response = await axios.post('http://localhost:8080/api/analyze', { text });
const result = response.data;
message.channel.send(`Analysis result: ${result.analysis}`);
} catch (error) {
console.error('Error analyzing text:', error);
message.channel.send('Sorry, I couldn\'t analyze the text at the moment.');
}
}
});

client.login(discordToken);

// API endpoint for AI analysis
app.post('/api/analyze', async (req, res) => {
const { text } = req.body;
try {
const response = await axios.post('https://api.openai.com/v1/engines/davinci-codex/completions', {
prompt: `Analyze the following text: ${text}`,
max_tokens: 50
}, {
headers: {
'Authorization': `Bearer ${openaiApiKey}`
}
});
const analysis = response.data.choices[0].text.trim();
res.json({ analysis });
} catch (error) {
console.error('Error analyzing text with OpenAI:', error);
res.status(500).json({ error: 'Failed to analyze text' });
}
});

app.listen(port, () => {
console.log(`Web app listening at http://localhost:${8080}`);
});
