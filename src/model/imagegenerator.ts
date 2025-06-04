export interface Env {
  AI: Ai;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    try {
      // Fetch a random cat image
      const res = await fetch("https://cataas.com/cat");

      if (!res.ok) {
        throw new Error(`Failed to fetch cat image: ${res.statusText}`);
      }

      const blob = await res.arrayBuffer();

      // Prepare inputs for AI model
      const inputs = {
        image: [...new Uint8Array(blob)],
      };

      // Run the AI model
      const response = await env.AI.run(
        "@cf/microsoft/resnet-50",
        inputs
      );

      // Return the AI model response
      return new Response(JSON.stringify(response), {
        headers: { "Content-Type": "application/json" },
      });

    } catch (error) {
      // Handle errors
      return new Response(`Error: ${error.message}`, { status: 500 });
    }
  },
} satisfies ExportedHandler<Env>;
