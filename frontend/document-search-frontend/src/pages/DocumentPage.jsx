import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

// Page to display a single document's full content
function DocumentPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [document, setDocument] = useState(null);

  // Fetch document data when component mounts or id changes
  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/api/document/${id}/`)
      .then((response) => {
        setDocument(response.data);
      })
      .catch((error) => {
        console.error("Error fetching document:", error);
      });
  }, [id]);

  if (!document) return <div>Loading full document...</div>;

  return (
    <div
      style={{
        padding: "20px",
        minHeight: "100vh",
        backgroundColor: "#f7f7f7",
      }}
    >
      <button
        onClick={() => navigate(-1)}
        style={{
          padding: "10px 20px",
          marginBottom: "20px",
          backgroundColor: "#007bff",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        ⬅️ Back to Search
      </button>

      <h1 style={{ marginBottom: "20px" }}>{document.title}</h1>
      <p style={{ whiteSpace: "pre-wrap", fontSize: "18px", color: "#333" }}>
        {document.content}
      </p>
    </div>
  );
}

export default DocumentPage;
