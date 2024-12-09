import React, { useState, useEffect } from 'react';
import axios from 'axios';

function FilterParts() {
    const [cpus, setCpus] = useState([]);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        axios.get('/cpu/info')
            .then(response => setCpus(response.data))
            .catch(error => console.error('Error fetching CPUs:', error));
    }, []);

    return (
        <div>
            <h1>Filter CPU Parts</h1>
            <input
                type="text"
                placeholder="Search by model..."
                onChange={e => setFilter(e.target.value)}
            />
            <ul>
                {cpus.filter(cpu => cpu.model.toLowerCase().includes(filter.toLowerCase())).map(filteredCpu => (
                    <li key={filteredCpu.cpuid}>{filteredCpu.model} - ${filteredCpu.price}</li>
                ))}
            </ul>
        </div>
    );
}

export default FilterParts;
