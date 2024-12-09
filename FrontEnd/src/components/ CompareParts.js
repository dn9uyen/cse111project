import React, { useState, useEffect } from 'react';
import { fetchAllComponents } from '../api/apiService';

function CompareParts({ componentType }) {
    const [parts, setParts] = useState([]);
    const [comparison, setComparison] = useState([]);

    useEffect(() => {
        const loadParts = async () => {
            try {
                const response = await fetchAllComponents(componentType);
                setParts(response.data);
            } catch (error) {
                console.error('Error fetching parts:', error);
            }
        };

        loadParts();
    }, [componentType]);

    const addToComparison = (id) => {
        const part = parts.find(p => p[`${componentType}id`] === parseInt(id));
        if (part && !comparison.find(c => c[`${componentType}id`] === part[`${componentType}id`])) {
            setComparison([...comparison, part]);
        }
    };

    return (
        <div>
            <h1>Compare {componentType} Parts</h1>
            <select onChange={(e) => addToComparison(e.target.value)}>
                <option value="">Select part to compare</option>
                {parts.map(part => (
                    <option key={part[`${componentType}id`]} value={part[`${componentType}id`]}>
                        {part.model}
                    </option>
                ))}
            </select>
            <div style={{ display: 'flex', gap: '20px' }}>
                {comparison.map(part => (
                    <div key={part[`${componentType}id`]}>
                        <h3>{part.model}</h3>
                        <p>Price: ${part.price}</p>
                        {/* Add other details for comparison */}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CompareParts;
