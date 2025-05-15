import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import UploadPage from "./pages/UploadPage";
import DocumentPage from "./pages/DocumentPage";
import Navbar from "./components/Navbar";

// Main App component that sets up routing
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/document/:id" element={<DocumentPage />} />
      </Routes>
    </Router>
  );
}

export default App;
