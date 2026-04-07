import React, { useState } from "react";
import axios from "axios";

const API_KEY = "default-dev-key";
const API_URL = "/api";

export default function FarmerForm() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [farmerId, setFarmerId] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function create() {
    setError("");
    
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/farmers/`, {
        name: name.trim(),
        phone: phone.trim() || null,
        language: "mr"
      }, {
        headers: {
          "x-api-key": API_KEY
        }
      });
      setFarmerId(res.data.id);
      setName("");
      setPhone("");
      // Auto-clear success message after 5 seconds
      setTimeout(() => setFarmerId(null), 5000);
    } catch (e) {
      // Handle Pydantic validation errors (422)
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
        setError("Error creating farmer: " + detail);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="form-container">
      <h3>➕ Create Farmer</h3>
      <div className="form-group">
        <label>Name (required)</label>
        <input 
          placeholder="Enter farmer name" 
          value={name} 
          onChange={e => setName(e.target.value)}
          disabled={loading}
        />
      </div>
      <div className="form-group">
        <label>Phone (optional)</label>
        <input 
          placeholder="Enter phone number" 
          value={phone} 
          onChange={e => setPhone(e.target.value)}
          disabled={loading}
        />
      </div>
      <button onClick={create} disabled={loading}>
        {loading ? "Creating..." : "Create Farmer"}
      </button>
      {error && <div className="alert alert-error">{error}</div>}
      {farmerId && (
        <div className="alert alert-success">
          ✓ Farmer created! ID: <strong>{farmerId}</strong>
        </div>
      )}
    </div>
  );
}