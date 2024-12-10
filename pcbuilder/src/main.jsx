import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';

function App() {
  const [data, setData] = useState('Select an option to get started!');

  // Generic API request function
  const handleApiRequest = async (endpoint, method = 'GET', body = null) => {
    const options = {
      method,
      headers: { 'Content-Type': 'application/json' },
      ...(body && { body: JSON.stringify(body) })
    };
    try {
      const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, options);
      const jsonData = await response.json();
      setData(JSON.stringify(jsonData, null, 2));
    } catch (error) {
      console.error('API request failed:', error);
      setData('Failed to fetch data');
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>PC Builder Tool</h1>
      <div>
        <button onClick={() => handleApiRequest('builds/new')}>Create a Build</button>
        <button onClick={() => handleApiRequest('parts/filter', 'POST', { price: 200, type: 'CPU' })}>Filter Parts</button>
        <button onClick={() => handleApiRequest('compatibility/check', 'POST', { cpuId: 1, ramId: 2 })}>Check Compatibility</button>
        <button onClick={() => handleApiRequest('builds/save', 'POST', { buildId: 123 })}>Save Build</button>
        <button onClick={() => handleApiRequest('builds/load?buildId=123')}>Load Build</button>
        <button onClick={() => handleApiRequest('parts/compare', 'POST', { partIds: [1, 2, 3] })}>Compare Parts</button>
        <button onClick={() => handleApiRequest('cpu/info?cpuid=1')}>View Component Details</button>
      </div>
      <section id="content-area" style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
        <pre>{data}</pre>
      </section>
    </div>
  );
}

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<App />);
} else {
  console.error('Failed to find the root element. Ensure your HTML file has an element with ID "root".');
}
