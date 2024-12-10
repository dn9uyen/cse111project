import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { createRoot } from 'react-dom/client';

function App() {
  return (
    <Router>
      <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        <h1>PC Builder Tool</h1>
        <nav>
          <ul>
            <li><Link to="/save-build">Save and Load Build</Link></li>
            <li><Link to="/filter-parts">Filter Parts</Link></li>
            <li><Link to="/compare-parts">Compare Parts</Link></li>
            <li><Link to="/view-component-details">View Component Details</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/save-build" element={<SaveBuild />} />
          <Route path="/filter-parts" element={<FilterParts />} />
          <Route path="/compare-parts" element={<CompareParts />} />
          <Route path="/view-component-details" element={<ViewComponentDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

function SaveBuild() {
  // Placeholder for your Save and Load build functionality
  return <div><h2>Save and Load Build Page</h2></div>;
}

function FilterParts() {
  // Placeholder, replace with actual filtering UI
  return <div><h2>Filter Parts Page</h2></div>;
}

function CompareParts() {
  // Placeholder, replace with actual comparison UI
  return <div><h2>Compare Parts Page</h2></div>;
}

function ViewComponentDetails() {
  // Placeholder, replace with actual view component details UI
  return <div><h2>View Component Details Page</h2></div>;
}

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<App />);
} else {
  console.error('Failed to find the root element. Ensure your HTML file has an element with ID "root".');
}
