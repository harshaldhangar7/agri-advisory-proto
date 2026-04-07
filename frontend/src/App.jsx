import React, { useState } from "react";
import { AuthProvider, useAuth } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import FarmerForm from "./components/FarmerForm";
import FarmerList from "./components/FarmerList";
import AdvisoryPanel from "./components/AdvisoryPanel";
import "./styles.css";

function AppContent() {
  const { isAuthenticated, user, logout, loading } = useAuth();

  if (loading) {
    return (
      <div className="app-container">
        <p style={{ textAlign: "center", paddingTop: "50px" }}>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginPage onLoginSuccess={() => {}} />;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>🌾 Agri Advisory Prototype</h1>
          <p>Smart agriculture advisory system for farmers</p>
        </div>
        <div className="header-user">
          <span className="user-name">Welcome, {user?.username}!</span>
          <button onClick={logout} className="logout-btn">
            Logout
          </button>
        </div>
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

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}