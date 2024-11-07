export interface Env {
  AI: Ai;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const response = await env.AI.run(
      "@cf/meta/llama-3.1-8b-instruct",
      {
        prompt: "Why should you use Cloudflare for your AI inference?",
      },
      {
        gateway: {
          id: "{f1b68c5fdd45d470836192141029a324}",
          skipCache: false,
          cacheTtl: 3360,
        },
      },
    );
    return new Response(JSON.stringify(response));
  },
} satisfies ExportedHandler<Env>;
