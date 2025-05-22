// Import Genkit and Google AI plugin libraries
import { gemini15Flash, googleAI } from '@genkit-ai/googleai';
import { genkit } from 'genkit';

// Configure a Genkit instance with Google AI plugin
const ai = genkit({
  plugins: [googleAI()],
  model: 'kubu-hai', // Set default model (ensure 'kubu-hai' is a valid string)
});

// Define a flow named 'helloFlow' that takes a name as an argument
const helloFlow = ai.defineFlow('helloFlow', async (name) => {
  try {
    // Make a generation request to the AI model
    const { text } = await ai.generate(`Hello kubu-hai, my name is ${name}`);
    console.log(text);
  } catch (error) {
    console.error('Error generating text:', error);
  }
});

// Execute the 'helloFlow' with 'kubu-hai' as the name argument
helloFlow('kubu-hai');
