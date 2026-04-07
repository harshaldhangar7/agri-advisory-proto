import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import PlotForm from "./PlotForm";

const API_URL = "/api";

export default function FarmerList() {
  const { accessToken } = useAuth();
  const [farmers, setFarmers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedFarmerId, setSelectedFarmerId] = useState(null);
  const [selectedFarmerData, setSelectedFarmerData] = useState(null);

  const fetchFarmers = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/farmers/`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      setFarmers(res.data);
    } catch (e) {
      setError("Error loading farmers: " + (e.response?.data?.detail || e.message));
    } finally {
      setLoading(false);
    }
  };

  const fetchFarmerDetail = async (farmerId) => {
    setError("");
    try {
      const res = await axios.get(`${API_URL}/farmers/${farmerId}`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      setSelectedFarmerData(res.data);
    } catch (e) {
      setError("Error loading farmer details: " + (e.response?.data?.detail || e.message));
    }
  };

  const deleteFarmer = async (farmerId) => {
    if (!window.confirm("Are you sure you want to delete this farmer?")) return;
    
    setError("");
    try {
      await axios.delete(`${API_URL}/farmers/${farmerId}`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      setFarmers(farmers.filter(f => f.id !== farmerId));
      setSelectedFarmerId(null);
      setSelectedFarmerData(null);
      alert("Farmer deleted successfully");
    } catch (e) {
      const detail = e.response?.data?.detail || e.message;
      setError("Error deleting farmer: " + detail);
    }
  };

  const deletePlot = async (farmerId, plotId) => {
    if (!window.confirm("Are you sure you want to delete this plot?")) return;
    
    setError("");
    try {
      await axios.delete(`${API_URL}/farmers/${farmerId}/plots/${plotId}`, {
        headers: { Authorization: `Bearer ${accessToken}` }
      });
      // Refresh farmer details
      fetchFarmerDetail(farmerId);
      alert("Plot deleted successfully");
    } catch (e) {
      const detail = e.response?.data?.detail || e.message;
      setError("Error deleting plot: " + detail);
    }
  };

  const handlePlotAdded = (newPlot) => {
    // Refresh farmer details after adding a plot
    if (selectedFarmerId) {
      fetchFarmerDetail(selectedFarmerId);
    }
  };

  useEffect(() => {
    fetchFarmers();
  }, []);

  return (
    <div style={{ border: "1px solid #ddd", padding: "15px", marginBottom: "15px", borderRadius: "5px" }}>
      <h3>Farmers List</h3>
      <button onClick={fetchFarmers} disabled={loading} style={{ marginBottom: "10px" }}>
        {loading ? "Loading..." : "Refresh"}
      </button>
      
      {error && <div style={{ color: "red", marginBottom: "10px" }}>{error}</div>}
      
      {farmers.length === 0 ? (
        <p>No farmers yet. Create one above!</p>
      ) : (
        <div>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ backgroundColor: "#f0f0f0" }}>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Name</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Phone</th>
                <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {farmers.map(farmer => (
                <tr key={farmer.id}>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{farmer.name}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>{farmer.phone || "-"}</td>
                  <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                    <button
                      onClick={() => {
                        setSelectedFarmerId(farmer.id);
                        fetchFarmerDetail(farmer.id);
                      }}
                      style={{ marginRight: "5px", padding: "5px 10px" }}
                    >
                      View
                    </button>
                    <button
                      onClick={() => deleteFarmer(farmer.id)}
                      style={{ padding: "5px 10px", backgroundColor: "#ff4444", color: "white", border: "none", cursor: "pointer" }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedFarmerData && (
        <div style={{ marginTop: "20px", padding: "10px", backgroundColor: "#f9f9f9", borderRadius: "5px" }}>
          <h4>Farmer Details: {selectedFarmerData.farmer.name}</h4>
          <p><strong>ID:</strong> {selectedFarmerData.farmer.id}</p>
          <p><strong>Phone:</strong> {selectedFarmerData.farmer.phone || "N/A"}</p>
          <p><strong>Language:</strong> {selectedFarmerData.farmer.language}</p>
          
          <h5>Plots ({selectedFarmerData.plots.length})</h5>
          {selectedFarmerData.plots.length === 0 ? (
            <p>No plots yet</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "10px" }}>
              <thead>
                <tr style={{ backgroundColor: "#f0f0f0" }}>
                  <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Name</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Crop</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Area (ha)</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {selectedFarmerData.plots.map(plot => (
                  <tr key={plot.id}>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{plot.name}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{plot.crop}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{plot.area_hectares}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                      <button
                        onClick={() => deletePlot(selectedFarmerId, plot.id)}
                        style={{ padding: "4px 8px", backgroundColor: "#ff4444", color: "white", border: "none", cursor: "pointer", borderRadius: "3px", fontSize: "12px" }}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {/* Add Plot Form */}
          <div style={{ marginTop: "15px", paddingTop: "15px", borderTop: "1px solid #ddd" }}>
            <PlotForm 
              farmerId={selectedFarmerId} 
              onPlotAdded={handlePlotAdded}
            />
          </div>
        </div>
      )}
    </div>
  );
}
