import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchComponentInfo } from '../api/apiService';

function ComponentDetails() {
    const { componentType, id } = useParams();
    const [component, setComponent] = useState(null);

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                const response = await fetchComponentInfo(componentType, id);
                setComponent(response.data);
            } catch (error) {
                console.error('Error fetching details:', error);
            }
        };

        fetchDetails();
    }, [componentType, id]);

    if (!component) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{component.model}</h1>
            <p>Price: ${component.price}</p>
            <p>Speed: {component.speed} GHz</p>
            <p>Boost Speed: {component.boostspeed} GHz</p>
            <p>Cores: {component.cores}</p>
            <p>Threads: {component.threads}</p>
            {/* Add more details as necessary */}
        </div>
    );
}

export default ComponentDetails;
