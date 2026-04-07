import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import "./LoginPage.css";

export default function LoginPage() {
  const { login, register, forgotPassword, resetPassword } = useAuth();
  const [mode, setMode] = useState("login"); // 'login', 'register', 'forgot'
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [resetEmail, setResetEmail] = useState("");
  const [resetCode, setResetCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [resetStep, setResetStep] = useState(1); // Step 1: Request, Step 2: Verify & Reset
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      if (mode === "login") {
        // Use AuthContext login
        await login(username.trim(), password);
      } else if (mode === "register") {
        // Register validation
        if (password !== confirmPassword) {
          setError("Passwords do not match");
          setLoading(false);
          return;
        }
        // Use AuthContext register
        await register(username.trim(), email.trim(), password);
      } else if (mode === "forgot") {
        if (resetStep === 1) {
          // Step 1: Request password reset using context function
          await forgotPassword(resetEmail.trim());
          setSuccess("Reset code sent to your email!");
          setResetStep(2);
        } else if (resetStep === 2) {
          // Step 2: Verify code and reset password using context function
          if (newPassword !== confirmNewPassword) {
            setError("Passwords do not match");
            setLoading(false);
            return;
          }
          await resetPassword(resetEmail.trim(), resetCode.trim(), newPassword.trim());
          setSuccess("✓ Password reset successful! Please login.");
          setTimeout(() => {
            setMode("login");
            setResetStep(1);
            setResetEmail("");
            setResetCode("");
            setNewPassword("");
            setConfirmNewPassword("");
            setSuccess("");
          }, 2000);
        }
      }
    } catch (err) {
      const detail = err.response?.data?.detail || err.message;
      setError(detail);
    } finally {
      setLoading(false);
    }
  }

  function resetForm() {
    setError("");
    setSuccess("");
    setUsername("");
    setEmail("");
    setPassword("");
    setConfirmPassword("");
    setResetEmail("");
    setResetCode("");
    setNewPassword("");
    setConfirmNewPassword("");
    setResetStep(1);
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>🌾 Agri Advisory</h1>
        <h2>
          {mode === "login" && "Login"}
          {mode === "register" && "Register"}
          {mode === "forgot" && "Reset Password"}
        </h2>

        <form onSubmit={handleSubmit}>
          {/* LOGIN FORM */}
          {mode === "login" && (
            <>
              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>
            </>
          )}

          {/* REGISTER FORM */}
          {mode === "register" && (
            <>
              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  placeholder="Enter email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  required
                />
                <small style={{ color: "#666", marginTop: "5px" }}>
                  Minimum 6 characters
                </small>
              </div>

              <div className="form-group">
                <label>Confirm Password</label>
                <input
                  type="password"
                  placeholder="Confirm password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>
            </>
          )}

          {/* FORGOT PASSWORD FORM */}
          {mode === "forgot" && (
            <>
              {resetStep === 1 && (
                <div className="form-group">
                  <label>Email Address</label>
                  <input
                    type="email"
                    placeholder="Enter your email"
                    value={resetEmail}
                    onChange={(e) => setResetEmail(e.target.value)}
                    disabled={loading}
                    required
                  />
                  <small style={{ color: "#666", marginTop: "5px" }}>
                    We'll send a reset code to this email
                  </small>
                </div>
              )}

              {resetStep === 2 && (
                <>
                  <div className="form-group">
                    <label>Reset Code</label>
                    <input
                      type="text"
                      placeholder="Enter code from email"
                      value={resetCode}
                      onChange={(e) => setResetCode(e.target.value)}
                      disabled={loading}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>New Password</label>
                    <input
                      type="password"
                      placeholder="Enter new password"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      disabled={loading}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Confirm Password</label>
                    <input
                      type="password"
                      placeholder="Confirm new password"
                      value={confirmNewPassword}
                      onChange={(e) => setConfirmNewPassword(e.target.value)}
                      disabled={loading}
                      required
                    />
                  </div>
                </>
              )}
            </>
          )}

          {error && <div className="alert alert-error">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}

          <button type="submit" disabled={loading} className="submit-btn">
            {loading
              ? mode === "login"
                ? "Logging in..."
                : mode === "register"
                ? "Registering..."
                : resetStep === 1
                ? "Sending Code..."
                : "Resetting Password..."
              : mode === "login"
              ? "Login"
              : mode === "register"
              ? "Register"
              : resetStep === 1
              ? "Send Reset Code"
              : "Reset Password"}
          </button>
        </form>

        <div className="toggle-form">
          {mode === "login" && (
            <>
              <p>
                Don't have an account?{" "}
                <button
                  type="button"
                  onClick={() => {
                    setMode("register");
                    resetForm();
                  }}
                  className="toggle-btn"
                >
                  Register
                </button>
              </p>
              <p>
                Forgot password?{" "}
                <button
                  type="button"
                  onClick={() => {
                    setMode("forgot");
                    resetForm();
                  }}
                  className="toggle-btn"
                >
                  Reset
                </button>
              </p>
            </>
          )}

          {mode === "register" && (
            <p>
              Already have an account?{" "}
              <button
                type="button"
                onClick={() => {
                  setMode("login");
                  resetForm();
                }}
                className="toggle-btn"
              >
                Login
              </button>
            </p>
          )}

          {mode === "forgot" && (
            <p>
              Remember password?{" "}
              <button
                type="button"
                onClick={() => {
                  setMode("login");
                  resetForm();
                }}
                className="toggle-btn"
              >
                Login
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}