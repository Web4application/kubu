export interface Env {
  AI: Ai;
}

export default {
  async fetch(request, env): Promise<Response> {
    const res = await fetch("https://cataas.com/cat");
    const blob = await res.arrayBuffer();

    const inputs = {
      image: [...new Uint8Array(blob)],
    };

    const response = await env.AI.run(
      "@cf/facebook/detr-resnet-50",
      inputs
    );

    return new Response(JSON.stringify({ inputs: { image: [] }, response }));
  },
} satisfies ExportedHandler<Env>;
