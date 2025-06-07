import { Configuration, OpenAIApi } from 'openai';
import axios from 'axios';

const configuration = new Configuration({
  apiKey: process.env.AIzaSyCHjfdo3w16ODd5yTVJD4o9pWmigOJEg,
});

const openai = new OpenAIApi(configuration);

export default async function handler(req, res) {
  const { prompt, functionType } = req.body;

  if (!prompt || !functionType) {
    return res.status(400).json({ error: 'Prompt and functionType are required' });
  }

  try {
    let response;
    switch (functionType) {
      case 'predictiveAnalytics':
        response = await openai.createCompletion({
          model: 'text-davinci-003',
          prompt: `Predictive Analytics: ${prompt}`,
          max_tokens: 150,
        });
        break;
      case 'marketAnalysis':
        response = await openai.createCompletion({
          model: 'text-davinci-003',
          prompt: `Market Analysis: ${prompt}`,
          max_tokens: 150,
        });
        break;
      case 'automatedTrading':
        response = await openai.createCompletion({
          model: 'text-davinci-003',
          prompt: `Automated Trading: ${prompt}`,
          max_tokens: 150,
        });
        break;
      case 'fraudDetection':
        response = await openai.createCompletion({
          model: 'text-davinci-003',
          prompt: `Fraud Detection: ${prompt}`,
          max_tokens: 150,
        });
        break;
      case 'sentimentAnalysis':
        response = await openai.createCompletion({
          model: 'text-davinci-003',
          prompt: `Sentiment Analysis: ${prompt}`,
          max_tokens: 150,
        });
        break;
      default:
        return res.status(400).json({ error: 'Invalid functionType' });
    }

    res.status(200).json({ response: response.data.choices[0].text });
  } catch (error) {
    res.status(500).json({ error: 'Error generating response' });
  }
}
