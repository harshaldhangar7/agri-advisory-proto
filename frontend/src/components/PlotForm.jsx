import React, { useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

const API_URL = "/api";

export default function PlotForm({ farmerId, onPlotAdded }) {
  const { accessToken } = useAuth();
  const [plotName, setPlotName] = useState("");
  const [crop, setCrop] = useState("");
  const [area, setArea] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function addPlot() {
    setError("");
    setSuccess("");
    
    // Validation
    if (!plotName.trim()) {
      setError("Plot name is required");
      return;
    }
    if (!crop.trim()) {
      setError("Crop name is required");
      return;
    }
    if (!area || area <= 0) {
      setError("Area must be greater than 0 hectares");
      return;
    }
    if (area > 10000) {
      setError("Area must be less than 10000 hectares");
      return;
    }
    
    setLoading(true);
    try {
      const res = await axios.post(
        `${API_URL}/farmers/${farmerId}/plots`,
        {
          name: plotName.trim(),
          crop: crop.trim(),
          area_hectares: parseFloat(area)
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        }
      );
      setSuccess(`✓ Plot "${plotName}" added successfully!`);
      setPlotName("");
      setCrop("");
      setArea("");
      
      // Callback to parent to refresh farmer details
      if (onPlotAdded) {
        onPlotAdded(res.data);
      }
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(""), 3000);
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
        setError("Error adding plot: " + detail);
      }
    } finally {
      setLoading(false);
    }
  }

  if (!farmerId) {
    return (
      <div className="form-container" style={{ opacity: 0.5 }}>
        <h4>➕ Add Plot</h4>
        <p style={{ color: "#999" }}>Select a farmer to add plots</p>
      </div>
    );
  }

  return (
    <div className="form-container">
      <h4>➕ Add Plot to Farmer</h4>
      
      <div className="form-group">
        <label>Plot Name (required)</label>
        <input
          placeholder="e.g., North Field, Field A"
          value={plotName}
          onChange={(e) => setPlotName(e.target.value)}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label>Crop Name (required)</label>
        <input
          placeholder="e.g., wheat, rice, cotton"
          value={crop}
          onChange={(e) => setCrop(e.target.value)}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label>Area (hectares, required)</label>
        <input
          type="number"
          placeholder="e.g., 5.5"
          step="0.1"
          min="0.1"
          max="10000"
          value={area}
          onChange={(e) => setArea(e.target.value)}
          disabled={loading}
        />
        <small style={{ color: "#666" }}>Must be between 0.1 and 10000 hectares</small>
      </div>

      <button onClick={addPlot} disabled={loading || !farmerId}>
        {loading ? "Adding..." : "Add Plot"}
      </button>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}
    </div>
  );
}
