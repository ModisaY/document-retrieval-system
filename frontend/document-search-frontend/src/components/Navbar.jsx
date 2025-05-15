// src/components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={{
      backgroundColor: "#007bff",
      padding: "15px",
      display: "flex",
      justifyContent: "center",
      gap: "30px",
      fontSize: "18px",
      fontWeight: "bold",
    }}>
      <Link to="/" style={{ color: "#fff", textDecoration: "none" }}>
        🔍 Search Documents
      </Link>
      <Link to="/upload" style={{ color: "#fff", textDecoration: "none" }}>
        📄 Upload Document
      </Link>
    </nav>
  );
}

export default Navbar;
