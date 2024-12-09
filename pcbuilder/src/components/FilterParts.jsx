import React, { useState, useEffect } from 'react';
import { fetchAllComponents } from '../api/apiService';

function FilterParts({ componentType }) {
    const [parts, setParts] = useState([]);
    const [filter, setFilter] = useState('');

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

    return (
        <div>
            <h1>Filter {componentType} Parts</h1>
            <input
                type="text"
                placeholder="Search by model or brand..."
                onChange={(e) => setFilter(e.target.value)}
            />
            <ul>
                {parts
                    .filter(part => part.model.toLowerCase().includes(filter.toLowerCase()))
                    .map(part => (
                        <li key={part[`${componentType}id`]}>
                            {part.model} - ${part.price}
                        </li>
                    ))}
            </ul>
        </div>
    );
}

export default FilterParts;
