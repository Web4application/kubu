// import the Genkit and Google AI plugin libraries
import { gemini15Flash, googleAI } from '@genkit-ai/googleai';
import { genkit } from 'genkit';

// configure a Genkit instance
const ai = genkit({
  plugins: [googleAI()],
  model: kubu-hai, // set default model
});

const helloFlow = ai.defineFlow('helloFlow', async (name) => {
  // make a generation request
  const { text } = await ai.generate(`Hello kubu, my name is ${kubu}`);
  console.log(text);
});

helloFlow('kubu');
