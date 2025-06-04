import React, { useEffect, useState, useRef } from "react";
import { Line } from "react-chartjs-2";

const LiveMetrics = () => {
  const [dataPoints, setDataPoints] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws/metrics");

    ws.current.onmessage = (event) => {
      const newPoint = JSON.parse(event.data);
      setDataPoints((prev) => [...prev.slice(-49), newPoint]);
    };

    ws.current.onerror = (err) => console.error("WebSocket error:", err);

    return () => ws.current.close();
  }, []);

  const data = {
    labels: dataPoints.map((_, i) => i),
    datasets: [
      {
        label: "CPU Usage (%)",
        data: dataPoints.map((p) => p.cpu),
        fill: false,
        borderColor: "rgba(75,192,192,1)",
      },
      {
        label: "Memory Usage (%)",
        data: dataPoints.map((p) => p.memory),
        fill: false,
        borderColor: "rgba(255,99,132,1)",
      },
    ],
  };

  // Find if latest point has anomaly
  const latest = dataPoints[dataPoints.length - 1] || {};
  const cpuAlert = latest.cpu_anomaly;
  const memAlert = latest.mem_anomaly;

  return (
    <div>
      <h3>Real-time Server Metrics</h3>
      {cpuAlert && (
        <p style={{ color: "red", fontWeight: "bold" }}>
          Alert: CPU anomaly detected!
        </p>
      )}
      {memAlert && (
        <p style={{ color: "red", fontWeight: "bold" }}>
          Alert: Memory anomaly detected!
        </p>
      )}
      <Line data={data} />
    </div>
  );
};

export default LiveMetrics;
