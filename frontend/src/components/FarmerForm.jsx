import React, { useState } from "react";
import axios from "axios";

export default function FarmerForm() {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [farmerId, setFarmerId] = useState(null);

  async function create() {
    try {
      const res = await axios.post("http://localhost:8000/api/farmers", {
        name,
        phone,
        language: "mr"
      });
      setFarmerId(res.data.id);
      alert("Farmer created: " + res.data.id);
    } catch (e) {
      alert("Error creating farmer: " + (e.response?.data?.detail || e.message));
    }
  }

  return (
    <div>
      <h3>Create Farmer</h3>
      <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
      <input placeholder="Phone" value={phone} onChange={e => setPhone(e.target.value)} />
      <button onClick={create}>Create</button>
      {farmerId && <div>Farmer ID: {farmerId}</div>}
    </div>
  );
}