// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import UploadPage from "./pages/UploadPage";
import Navbar from "./components/Navbar"; // Import navbar

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<SearchPage />} />
        <Route path="/upload" element={<UploadPage />} />
      </Routes>
    </Router>
  );
}

export default App;
