import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

// Page for searching documents and displaying results
function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // Handles the search form submission
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/search/?q=${query}`
      );
      setResults(response.data.results);
    } catch (error) {
      console.error("Error searching:", error);
    }
    setLoading(false);
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
        🔍 Document Search
      </h1>

      {/* Search Form */}
      <form
        onSubmit={handleSearch}
        style={{
          display: "flex",
          justifyContent: "center",
          marginBottom: "30px",
        }}
      >
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your search keyword..."
          style={{
            width: "400px",
            padding: "10px 15px",
            fontSize: "16px",
            border: "1px solid #ccc",
            borderRadius: "8px 0 0 8px",
            outline: "none",
          }}
          required
        />
        <button
          type="submit"
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            backgroundColor: "#007bff",
            color: "#fff",
            border: "none",
            borderRadius: "0 8px 8px 0",
            cursor: "pointer",
          }}
        >
          Search
        </button>
      </form>

      {/* Search Results */}
      {loading ? (
        <div style={{ textAlign: "center", fontSize: "18px" }}>
          Searching...
        </div>
      ) : (
        <div style={{ maxWidth: "900px", margin: "0 auto" }}>
          {results.length > 0 ? (
            results.map((doc) => (
              <div
                key={doc.id}
                style={{
                  backgroundColor: "#fff",
                  padding: "20px",
                  marginBottom: "20px",
                  borderRadius: "10px",
                  boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                }}
              >
                {/* Clickable Title */}
                <Link
                  to={`/document/${doc.id}`}
                  style={{ textDecoration: "none", color: "#007bff" }}
                >
                  <h2>{doc.title}</h2>
                </Link>

                {/* Content Preview */}
                <p style={{ color: "#555", marginBottom: "10px" }}>
                  {doc.content_preview}
                </p>

                {/* TF-IDF Score */}
                <p style={{ fontWeight: "bold", color: "#333" }}>
                  Score: {doc.score}
                </p>
              </div>
            ))
          ) : (
            <p style={{ textAlign: "center", color: "#777" }}>
              No results to show.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default SearchPage;
