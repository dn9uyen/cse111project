import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CompareParts() {
    const [cpus, setCpus] = useState([]);
    const [comparison, setComparison] = useState([]);

    useEffect(() => {
        axios.get('/cpu/info')
            .then(response => setCpus(response.data))
            .catch(error => console.error('Error fetching CPUs:', error));
    }, []);

    const addToComparison = cpuid => {
        const cpu = cpus.find(c => c.cpuid === parseInt(cpuid));
        if (cpu && !comparison.find(c => c.cpuid === cpu.cpuid)) {
            setComparison([...comparison, cpu]);
        }
    };

    return (
        <div>
            <h1>Compare CPUs</h1>
            <select onChange={e => addToComparison(e.target.value)}>
                <option value="">Select CPU to compare</option>
                {cpus.map(cpu => (
                    <option key={cpu.cpuid} value={cpu.cpuid}>{cpu.model}</option>
                ))}
            </select>
            <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                {comparison.map(cpu => (
                    <div key={cpu.cpuid}>
                        <h2>{cpu.model}</h2>
                        <p>Price: ${cpu.price}</p>
                        <p>Speed: {cpu.speed} GHz</p>
                        {/* Display more CPU details if we need */}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CompareParts;
