import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import AdminDashboard from "./AdminDashboard";
import Login from "./login"; 
import EmployeeDashboard from "./EmployeeDashboard"; 

// ProtectedRoute component to restrict access based on role
function ProtectedRoute({ user, allowedRole, children }) {
  if (!user) {
    // Redirect to login if no user is authenticated
    return <Navigate to="/" replace />;
  }
  if (user.role !== allowedRole) {
    // Redirect to unauthorized or employee dashboard if role doesn't match
    return <Navigate to={user.role === "employee" ? "/employee" : "/"} replace />;
  }
  return children;
}

function App() {
  const [user, setUser] = useState(null); // Store authenticated user

  // Logout function to clear user and token
  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <Router>
      <Routes>
        {/* Login route */}
        <Route path="/" element={<Login setUser={setUser} />} />

        {/* Admin route: only accessible to users with role "admin" */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute user={user} allowedRole="admin">
              <AdminDashboard user={user} onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />

        {/* Employee route: only accessible to users with role "employee" */}
        <Route
          path="/employee"
          element={
            <ProtectedRoute user={user} allowedRole="employee">
              <EmployeeDashboard user={user} onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />

        {/* Fallback for unknown routes */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;