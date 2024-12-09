import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CreateBuild() {
    const [cpus, setCpus] = useState([]);
    const [selectedCpu, setSelectedCpu] = useState('');

    useEffect(() => {
        axios.get('/cpu/info')
            .then(response => setCpus(response.data))
            .catch(error => console.error('Error fetching CPUs:', error));
    }, []);

    return (
        <div>
            <h1>Create Your PC Build</h1>
            <label htmlFor="cpu-select">Choose a CPU:</label>
            <select id="cpu-select" value={selectedCpu} onChange={e => setSelectedCpu(e.target.value)}>
                {cpus.map(cpu => (
                    <option key={cpu.cpuid} value={cpu.cpuid}>{cpu.model}</option>
                ))}
            </select>
            {/* Implement other components If we need */}
        </div>
    );
}

export default CreateBuild;
