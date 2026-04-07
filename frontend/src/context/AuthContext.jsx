import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

export const AuthContext = createContext();

const API_URL = "/api/auth";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    const storedUser = localStorage.getItem("user");
    const storedRefreshToken = localStorage.getItem("refresh_token");

    if (storedToken && storedUser) {
      setAccessToken(storedToken);
      setRefreshToken(storedRefreshToken);
      setUser(JSON.parse(storedUser));
    }

    setLoading(false);
  }, []);

  // Setup axios interceptor for token refresh
  useEffect(() => {
    if (!accessToken) return;

    const interceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // If 401 and not already retried, try to refresh token
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const response = await axios.post(`${API_URL}/refresh`, {}, {
              headers: {
                Authorization: `Bearer ${refreshToken}`,
              },
            });

            const { access_token, refresh_token } = response.data;

            setAccessToken(access_token);
            setRefreshToken(refresh_token);
            localStorage.setItem("access_token", access_token);
            localStorage.setItem("refresh_token", refresh_token);

            // Retry original request with new token
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return axios(originalRequest);
          } catch (refreshError) {
            // Refresh failed, logout user
            logout();
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, [accessToken, refreshToken]);

  // Set default authorization header
  useEffect(() => {
    if (accessToken) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;
    } else {
      delete axios.defaults.headers.common["Authorization"];
    }
  }, [accessToken]);

  async function login(username, password) {
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/login`, {
        username,
        password,
      });

      const { access_token, refresh_token, user: userData } = response.data;

      setAccessToken(access_token);
      setRefreshToken(refresh_token);
      setUser(userData);

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);
      localStorage.setItem("user", JSON.stringify(userData));

      return userData;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Login failed";
      setError(errorMsg);
      throw err;
    }
  }

  async function register(username, email, password) {
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/register`, {
        username,
        email,
        password,
      });

      const { access_token, refresh_token, user: userData } = response.data;

      setAccessToken(access_token);
      setRefreshToken(refresh_token);
      setUser(userData);

      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);
      localStorage.setItem("user", JSON.stringify(userData));

      return userData;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Registration failed";
      setError(errorMsg);
      throw err;
    }
  }

  function logout() {
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");

    delete axios.defaults.headers.common["Authorization"];
  }

  async function forgotPassword(email) {
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/forgot-password`, { email });
      return response.data; // Contains { message, reset_code }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Failed to request password reset";
      setError(errorMsg);
      throw err;
    }
  }

  async function resetPassword(email, resetCode, newPassword) {
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/reset-password`, {
        email,
        reset_code: resetCode,
        new_password: newPassword,
      });
      return response.data; // Contains { message }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Failed to reset password";
      setError(errorMsg);
      throw err;
    }
  }

  const value = {
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
