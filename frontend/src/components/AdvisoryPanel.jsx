import React, { useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

const API_URL = "/api";

export default function AdvisoryPanel() {
  const { accessToken } = useAuth();
  const [plotId, setPlotId] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [advice, setAdvice] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function getAdvice() {
    setError("");
    setAdvice(null);
    
    if (!plotId.trim()) {
      setError("Plot ID is required");
      return;
    }
    
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/advisory/recommend`, {
        plot_id: plotId.trim(),
        symptoms: symptoms.trim() || null,
        weather: { rain_last_3_days: 0 }
      }, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
      setAdvice(res.data.advice);
    } catch (e) {
      // Handle validation errors
      if (e.response?.status === 422) {
        const errors = e.response?.data?.detail || [];
        if (Array.isArray(errors)) {
          const errorMsg = errors.map(err => `${err.loc[1]}: ${err.msg}`).join(", ");
          setError("Validation Error: " + errorMsg);
        } else {
          setError("Validation Error: " + JSON.stringify(errors));
        }
      } else {
        const detail = e.response?.data?.detail || e.message;
        setError("Error: " + detail);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="form-container">
      <h3>💡 Get Advisory</h3>
      <div className="form-group">
        <label>Plot ID (required)</label>
        <input 
          placeholder="Enter plot ID" 
          value={plotId} 
          onChange={e => setPlotId(e.target.value)}
          disabled={loading}
        />
      </div>
      <div className="form-group">
        <label>Symptoms (optional)</label>
        <textarea 
          placeholder="Describe crop symptoms (e.g., yellow leaves, brown spots)" 
          value={symptoms} 
          onChange={e => setSymptoms(e.target.value)}
          disabled={loading}
        />
      </div>
      <button onClick={getAdvice} disabled={loading}>
        {loading ? "Getting advice..." : "Get Advice"}
      </button>
      {error && <div className="alert alert-error">{error}</div>}
      {advice && (
        <div style={{ marginTop: "20px", padding: "15px", backgroundColor: "#f9f9f9", borderRadius: "5px", borderLeft: "4px solid #2d7a3e" }}>
          <h4>✓ Advisory for Plot {plotId}</h4>
          <ul className="advice-list">
            {advice.map((a, i) => (
              <li key={i}>{a}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}