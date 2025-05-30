import React, { useState } from "react";

export default function KubuHaiUI() {
  const [repoUrl, setRepoUrl] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function analyzeRepo() {
    setLoading(true);
    setError(null);
    setSummary(null);
    try {
      const res = await fetch(`/clone-analyze?git_url=${encodeURIComponent(repoUrl)}`);
      if (!res.ok) throw new Error(`API error: ${res.statusText}`);
      const data = await res.json();
      setSummary(data.summary);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Kubu-hai Repo Analyzer</h1>
      <input
        type="text"
        placeholder="Enter GitHub repo URL"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
      />
      <button
        onClick={analyzeRepo}
        disabled={!repoUrl || loading}
        style={{ marginTop: "1rem", padding: "0.5rem 1rem", fontSize: "1rem" }}
      >
        {loading ? "Analyzing..." : "Analyze Repo"}
      </button>

      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {summary && (
        <pre
          style={{
            marginTop: "2rem",
            background: "#f0f0f0",
            padding: "1rem",
            whiteSpace: "pre-wrap",
            borderRadius: "6px",
          }}
        >
          {summary}
        </pre>
      )}
    </div>
  );
}
