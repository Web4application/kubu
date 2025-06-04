import React, { useState } from "react";

export default function KubuHaiUI() {
  const [repoUrl, setRepoUrl] = useState("");
  const [projectId, setProjectId] = useState(null);
  const [summary, setSummary] = useState(null);
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const apiBase = "/api"; // nginx proxy

  async function cloneAnalyze() {
    setLoading(true);
    setMessage("");
    setSummary(null);
    setFiles([]);
    try {
      const res = await fetch(`${apiBase}/clone-analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ git_url: repoUrl }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setSummary(data.summary);
      setProjectId(data.project_id);
    } catch (e) {
      setMessage(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function upgradeProject() {
    if (!projectId) return;
    setLoading(true);
    setMessage("");
    try {
      const res = await fetch(`${apiBase}/upgrade-project/${projectId}`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setMessage(data.message);
    } catch (e) {
      setMessage(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function generateReadme() {
    if (!projectId) return;
    setLoading(true);
    setMessage("");
    try {
      const res = await fetch(`${apiBase}/generate-readme/${projectId}`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setMessage(data.message);
    } catch (e) {
      setMessage(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function installDeps() {
    if (!projectId) return;
    setLoading(true);
    setMessage("");
    try {
      const res = await fetch(`${apiBase}/install-dependencies/${projectId}`, { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setMessage(data.message);
    } catch (e) {
      setMessage(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function listFiles() {
    if (!projectId) return;
    setLoading(true);
    setMessage("");
    try {
      const res = await fetch(`${apiBase}/project-files/${projectId}`);
      const data = await res.json();
      if (!res.ok) throw new Error("Failed to fetch files");
      setFiles(data.files);
    } catch (e) {
      setMessage(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 700, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>Kubu-hai Project AI Assistant</h1>

      <input
        type="text"
        placeholder="Enter GitHub repo URL"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
      />

      <button
        disabled={!repoUrl || loading}
        onClick={cloneAnalyze}
        style={{ marginTop: "1rem", padding: "0.5rem 1rem", fontSize: "1rem" }}
      >
        {loading ? "Working..." : "Clone & Analyze"}
      </button>

      {summary && (
        <>
          <h2>Summary</h2>
          <pre style={{ background: "#f0f0f0", padding: "1rem", borderRadius: "6px" }}>{summary}</pre>
          <div style={{ marginTop: "1rem" }}>
            <button onClick={upgradeProject} disabled={loading}>Upgrade Project</button>
            <button onClick={generateReadme} disabled={loading} style={{ marginLeft: "1rem" }}>Generate README</button>
            <button onClick={installDeps} disabled={loading} style={{ marginLeft: "1rem" }}>Install Dependencies</button>
            <button onClick={listFiles} disabled={loading} style={{ marginLeft: "1rem" }}>List Files</button>
          </div>
        </>
      )}

      {message && <p style={{ color: "red", marginTop: "1rem" }}>{message}</p>}

      {files.length > 0 && (
        <>
          <h3>Project Files</h3>
          <ul>
            {files.map((f) => (
              <li key={f}>{f}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
