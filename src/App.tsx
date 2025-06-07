import React, { useState } from 'react';

function App() {
  const [repoUrl, setRepoUrl] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setIsLoading(true);
    setResult(null);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/analyzeRepo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repoUrl }),
      });
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const data = await response.json();
      setResult(data.summary);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: 'sans-serif', maxWidth: 700, margin: 'auto' }}>
      <h1>GitHub Repo AI Analyzer</h1>
      <input
        type="text"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
        placeholder="Enter GitHub repo URL"
        style={{ width: '100%', padding: 8, fontSize: 16 }}
      />
      <button
        onClick={handleAnalyze}
        disabled={!repoUrl || isLoading}
        style={{ marginTop: 12, padding: '10px 20px', fontSize: 16 }}
      >
        {isLoading ? 'Analyzing...' : 'Analyze'}
      </button>

      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {result && (
        <pre
          style={{
            whiteSpace: 'pre-wrap',
            backgroundColor: '#f0f0f0',
            marginTop: 20,
            padding: 15,
            borderRadius: 6,
          }}
        >
          {result}
        </pre>
      )}
    </div>
  );
}

export default App;
