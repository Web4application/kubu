import React from "react";
import LiveMetrics from "./LiveMetrics";

function App() {
  return (
    <div style={{ maxWidth: 900, margin: "auto", padding: 20, fontFamily: "Arial" }}>
      <h1>Kubu-Hai Real-time Metrics Dashboard</h1>
      <LiveMetrics />
    </div>
  );
}

export default App;
