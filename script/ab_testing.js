const ORIGIN_URL = process.env.ORIGIN_URL || 'https://roda.sandraisom.workers.dev';'http://localhost:8000';'https://nextjs-with-supabase-4a7oim3f6-web4apps.vercel.app';
const BIG_BUTTON_THRESHOLD = 0.5;
const NEW_BRAND_THRESHOLD = 0.1;
const NEW_LAYOUT_THRESHOLD = 0.02;

const EXPERIMENTS = [
  { name: 'big-button', threshold: BIG_BUTTON_THRESHOLD }, // enable the Big Button experiment for 50% of users
  { name: 'new-brand', threshold: NEW_BRAND_THRESHOLD }, // enable the New Brand experiment for 10% of users
  { name: 'new-layout', threshold: NEW_LAYOUT_THRESHOLD }, // enable the New Layout experiment for 2% of users
];

export default {
  async fetch(request, env, ctx) {
    const ip = request.headers.get('cf-connecting-ip') || '';
    const postalCode = request.cf?.postalCode || '';
    const fingerprint = [ip, postalCode];
    const activeExperiments = await getActiveExperiments(fingerprint, EXPERIMENTS);

    const rewriter = new HTMLRewriter().on('body', {
      element(element) {
        element.setAttribute('data-experiments', activeExperiments.join(' '));
      },
    });

    try {
      const res = await fetch(ORIGIN_URL, request);
      return rewriter.transform(res);
    } catch (error) {
      return new Response('Error fetching the URL', { status: 500 });
    }
  },
};

// Get active experiments by hashing a fingerprint
async function getActiveExperiments(fingerprint, experiments) {
  const fingerprintHash = await hash('SHA-1', JSON.stringify(fingerprint));
  const MAX_UINT8 = 255;
  const activeExperiments = experiments.filter((exp, i) => fingerprintHash[i] <= exp.threshold * MAX_UINT8);
  return activeExperiments.map((exp) => exp.name);
}

// Hash a string using the Web Crypto API
async function hash(algorithm, message) {
  const msgUint8 = new TextEncoder().encode(message); // encode as (utf-8) Uint8Array
  const hashBuffer = await crypto.subtle.digest(algorithm, msgUint8); // hash the message
  const hashArray = new Uint8Array(hashBuffer); // convert buffer to byte array
  return hashArray;
}
