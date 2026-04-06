import React from "react";
import FarmerForm from "./components/FarmerForm";
import AdvisoryPanel from "./components/AdvisoryPanel";

export default function App() {
  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h2>Agri Advisory Prototype</h2>
      <FarmerForm />
      <hr />
      <AdvisoryPanel />
    </div>
  );
}