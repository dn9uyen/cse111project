import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

function PartDetails() {
    const [cpu, setCpu] = useState(null);
    const { cpuid } = useParams();

    useEffect(() => {
        axios.get(`/cpu/info?cpuid=${cpuid}`)
            .then(response => {
                setCpu(response.data);
            })
            .catch(error => console.error('Error fetching CPU details:', error));
    }, [cpuid]);

    if (!cpu) return <div>Loading...</div>;

    return (
        <div>
            <h1>{cpu.model}</h1>
            <p>Price: ${cpu.price}</p>
            <p>Speed: {cpu.speed} GHz</p>
            <p>Boost Speed: {cpu.boostspeed} GHz</p>
            <p>Cores: {cpu.cores}</p>
            {/* Add more details if we need */}
        </div>
    );
}

export default PartDetails;
