function createSimplePrompt() {
  return { prompt: 'Tell me a joke about Cloudflare' };
}

function createChatMessages() {
  return {
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'Who won the world series in 2020?' }
    ]
  };
}

async function processAIRequest(env, input) {
  return await env.AI.run('@cf/meta/llama-3-8b-instruct', input);
}

export default {
  async fetch(request, env) {
    const tasks = [];
    try {
      let simple = createSimplePrompt();
      let response = await processAIRequest(env, simple);
      tasks.push({ inputs: simple, response });

      let chat = createChatMessages();
      response = await processAIRequest(env, chat);
      tasks.push({ inputs: chat, response });

      return new Response(JSON.stringify(tasks), { status: 200 });
    } catch (error) {
      return new Response(`Error: ${error.message}`, { status: 500 });
    }
  }
}
