// src/pages/UploadPage.jsx
import React, { useState } from "react";
import axios from "axios";

// Page for uploading a new text document
function UploadPage() {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  // Handles file input change
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handles the upload form submission
  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("❌ Please select a .txt file.");
      return;
    }

    const reader = new FileReader();
    reader.onload = async (event) => {
      const fileContent = event.target.result;

      try {
        const payload = {
          title: title || file.name.replace(".txt", ""),
          content: fileContent,
        };

        await axios.post(
          "http://127.0.0.1:8000/api/upload/",
          JSON.stringify(payload),
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        setMessage("✅ Document uploaded successfully!");
        setTitle("");
        setFile(null);
      } catch (error) {
        console.error(
          "Error uploading document:",
          error.response?.data || error.message
        );
        setMessage(
          "❌ Error uploading document. Please check file format or server."
        );
      }
    };

    reader.readAsText(file);
  };

  return (
    <div
      style={{
        padding: "20px",
        minHeight: "100vh",
        backgroundColor: "#f7f7f7",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
        📄 Upload Text Document
      </h1>

      <form
        onSubmit={handleUpload}
        style={{
          backgroundColor: "#fff",
          padding: "30px",
          borderRadius: "10px",
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
          maxWidth: "600px",
          margin: "0 auto",
          display: "flex",
          flexDirection: "column",
          gap: "20px",
        }}
      >
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter title (optional)"
          style={{
            padding: "10px",
            fontSize: "16px",
            borderRadius: "8px",
            border: "1px solid #ccc",
          }}
        />

        <input
          type="file"
          accept=".txt"
          onChange={handleFileChange}
          required
          style={{ padding: "10px", fontSize: "16px" }}
        />

        <button
          type="submit"
          style={{
            padding: "12px",
            fontSize: "18px",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
          }}
        >
          Upload
        </button>

        {message && (
          <p
            style={{
              marginTop: "10px",
              fontWeight: "bold",
              textAlign: "center",
              color: message.startsWith("✅") ? "green" : "red",
            }}
          >
            {message}
          </p>
        )}
      </form>
    </div>
  );
}

export default UploadPage;
