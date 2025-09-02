import React, { useState } from "react";
import axios from "axios";

export default function Login({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!role) {
      setError("Please select a role.");
      return;
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/auth/login", {
        email,
        password,
        role, // ✅ sending role to backend
      });

      // Save token
      localStorage.setItem("token", res.data.access_token);

      // ✅ Make sure user object has email + role
      setUser({
        email: res.data.user?.email || email,
        role: res.data.user?.role || role,
      });

    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || "Login failed! Please check your credentials.";
      setError(errorMessage);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", padding: "20px" }}>
      <h2>Login Page</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
            required
          />
        </div>
        <div>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
            required
          >
            <option value="" disabled>
              Select Role
            </option>
            <option value="admin">Admin</option>
            <option value="employee">Employee</option>
            <option value="employer">Employer</option> {/* ✅ added */}
          </select>
        </div>
        <button type="submit" style={{ padding: "8px 16px" }}>
          Login
        </button>
      </form>
    </div>
  );
}
