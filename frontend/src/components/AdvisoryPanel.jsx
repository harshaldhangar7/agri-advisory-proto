import React, { useState } from "react";
import axios from "axios";

export default function AdvisoryPanel() {
  const [plotId, setPlotId] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [advice, setAdvice] = useState(null);

  async function getAdvice() {
    try {
      const res = await axios.post("http://localhost:8000/api/advisory/recommend", {
        plot_id: plotId,
        symptoms,
        weather: { rain_last_3_days: 0 }
      });
      setAdvice(res.data.advice);
    } catch (e) {
      alert("Error: " + (e.response?.data?.detail || e.message));
    }
  }

  return (
    <div>
      <h3>Get Advisory</h3>
      <input placeholder="Plot ID" value={plotId} onChange={e => setPlotId(e.target.value)} />
      <input placeholder="Symptoms (e.g., yellow leaves)" value={symptoms} onChange={e => setSymptoms(e.target.value)} />
      <button onClick={getAdvice}>Get Advice</button>
      {advice && (
        <div>
          <h4>Advice</h4>
          <ul>{advice.map((a, i) => <li key={i}>{a}</li>)}</ul>
        </div>
      )}
    </div>
  );
}