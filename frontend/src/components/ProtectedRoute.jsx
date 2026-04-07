import React from "react";
import { useAuth } from "../context/AuthContext";

export function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
      }}>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will be handled by App.jsx routing
  }

  return children;
}
