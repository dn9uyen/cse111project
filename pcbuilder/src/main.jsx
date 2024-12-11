import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { getPartInfo, getTable } from './api'; // Adjust the path as necessary

function App() {
    const [data, setData] = useState('Select an option to get started!');
    const [error, setError] = useState('');

    // Fetch part info by type and id
    const fetchPartInfo = async (partType, partId) => {
        try {
            const info = await getPartInfo(partType, partId);
            setData(JSON.stringify(info, null, 2));
            setError('');
        } catch (err) {
            setError(`Failed to fetch ${partType} data`);
            console.error('API request failed:', err);
        }
    };

    // Get table info (e.g., brands)
    const handleGetTable = async (tableName) => {
        try {
            const tableInfo = await getTable(tableName);
            setData(JSON.stringify(tableInfo, null, 2));
            setError('');
        } catch (err) {
            setError(`Failed to fetch ${tableName}`);
            console.error('API request failed:', err);
        }
    };

    // Display all parts types available in the system
    const partTypes = ['cpu', 'ram', 'motherboard', 'psu', 'gpu', 'storage', 'cooler'];

    return (
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif", display: "flex", flexDirection: "column", alignItems: "center" }}>
            <h1>PC Builder Tool</h1>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <div>
                {partTypes.map((partType) => (
                    <button key={partType} onClick={() => fetchPartInfo(partType, 1)} style={{ margin: "5px" }}>
                        Choose {partType.toUpperCase()}
                    </button>
                ))}
                <button onClick={() => handleGetTable('brand')} style={{ margin: "5px" }}>
                    Get Brands
                </button>
            </div>
            <div style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
                <pre>{data}</pre>
            </div>
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
