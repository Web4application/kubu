require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const { Client, GatewayIntentBits } = require('discord.js');
const winston = require('winston');
const rateLimit = require('express-rate-limit');

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Logging setup
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
    ],
});

// Discord bot setup
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });
const discordToken = process.env.DISCORD_TOKEN;
const openaiApiKey = process.env.OPENAI_API_KEY;

client.once('ready', () => {
    logger.info('Discord bot is online!');
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
            logger.error('Error analyzing text:', error);
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
        logger.error('Error analyzing text with OpenAI:', error);
        res.status(500).json({ error: 'Failed to analyze text' });
    }
});

app.listen(port, () => {
    logger.info(`Web app listening at http://localhost:${port}`);
});

// Error handling middleware
app.use((err, req, res, next) => {
    logger.error(err.stack);
    res.status(500).send('Something broke!');
});
