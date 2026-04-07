import React from "react";
import FarmerForm from "./components/FarmerForm";
import FarmerList from "./components/FarmerList";
import AdvisoryPanel from "./components/AdvisoryPanel";
import "./styles.css";

export default function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🌾 Agri Advisory Prototype</h1>
        <p>Smart agriculture advisory system for farmers</p>
      </header>

      <main className="app-main">
        <section className="section">
          <FarmerForm />
        </section>

        <section className="section">
          <FarmerList />
        </section>

        <section className="section">
          <AdvisoryPanel />
        </section>
      </main>

      <footer className="app-footer">
        <p>&copy; 2026 Agri Advisory. All rights reserved.</p>
      </footer>
    </div>
  );
}