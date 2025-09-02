import React from "react";

export default function EmployeeDashboard({ user, onLogout }) {
  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Employee Dashboard</h1>
      <p>Welcome, {user?.email || "Employee"}!</p>
      <p>This is a view-only dashboard for employees. You can view content but cannot edit or manage it.</p>
      <button onClick={onLogout} style={{ padding: "8px 16px", marginTop: "10px" }}>
        Logout
      </button>
    </div>
  );
}