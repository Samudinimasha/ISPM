import React, { useState } from "react";
import axios from "axios";

export default function AdminDashboard({ user, onLogout }) {
  const [registerUser, setRegisterUser] = useState({ email: "", password: "", role: "employee" });
  const [updateUser, setUpdateUser] = useState({ userId: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleRegisterUser = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const token = localStorage.getItem("token");
      await axios.post(
        "http://127.0.0.1:8000/auth/register", // Use /auth/register endpoint
        registerUser,
        { headers: { Authorization: `Bearer ${token}` } } // Include token for admin check
      );
      setSuccess("User registered successfully!");
      setRegisterUser({ email: "", password: "", role: "employee" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to register user");
    }
  };

  const handleUpdateUser = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const token = localStorage.getItem("token");
      await axios.put(
        `http://127.0.0.1:8000/auth/users/${updateUser.userId}`,
        { email: updateUser.email || null, password: updateUser.password || null },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess("User updated successfully!");
      setUpdateUser({ userId: "", email: "", password: "" });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update user");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Admin Panel</h1>
      <p>Welcome, {user?.email || "Admin"}!</p>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}

      <h3>Register New User</h3>
      <form onSubmit={handleRegisterUser}>
        <div>
          <input
            type="email"
            placeholder="Email"
            value={registerUser.email}
            onChange={(e) => setRegisterUser({ ...registerUser, email: e.target.value })}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={registerUser.password}
            onChange={(e) => setRegisterUser({ ...registerUser, password: e.target.value })}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
            required
          />
        </div>
        <div>
          <select
            value={registerUser.role}
            onChange={(e) => setRegisterUser({ ...registerUser, role: e.target.value })}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
            required
          >
            <option value="admin">Admin</option>
            <option value="employee">Employee</option>
          </select>
        </div>
        <button type="submit" style={{ padding: "8px 16px", margin: "8px 0" }}>
          Register User
        </button>
      </form>

      <h3>Update User</h3>
      <form onSubmit={handleUpdateUser}>
        <div>
          <input
            type="number"
            placeholder="User ID"
            value={updateUser.userId}
            onChange={(e) => setUpdateUser({ ...updateUser, userId: e.target.value })}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
            required
          />
        </div>
        <div>
          <input
            type="email"
            placeholder="New Email (optional)"
            value={updateUser.email}
            onChange={(e) => setUpdateUser({ ...updateUser, email: e.target.value })}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="New Password (optional)"
            value={updateUser.password}
            onChange={(e) => setUpdateUser({ ...updateUser, password: e.target.value })}
            style={{ width: "100%", padding: "8px", margin: "8px 0" }}
          />
        </div>
        <button type="submit" style={{ padding: "8px 16px", margin: "8px 0" }}>
          Update User
        </button>
      </form>

      <button onClick={onLogout} style={{ padding: "8px 16px", marginTop: "10px" }}>
        Logout
      </button>
    </div>
  );
}