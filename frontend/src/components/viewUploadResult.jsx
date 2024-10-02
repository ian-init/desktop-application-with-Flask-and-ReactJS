import React, { useState, useEffect } from 'react';

const NewComponent = () => {
    const [length, setLength] = useState(null); // State to store the length

    // Fetch the length from the backend when the component mounts
    useEffect(() => {
        const fetchLength = async () => {
            try {
                const response = await fetch(`http://localhost:5000/get-length`); // Make sure this endpoint returns the length
                const result = await response.json();

                if (response.ok) {
                    setLength(result.length); // Set the length received from the backend
                } else {
                    console.error("Error:", result.error);
                }
            } catch (error) {
                console.error("Error:", error);
            }
        };

        fetchLength();
    }, );

    return (
        <div>
            <h1>File Information</h1>
            {length !== null ? (
                <div>
                    <h2>File Length: {length}</h2>
                </div>
            ) : (
                <p>Loading file length...</p>
            )}
        </div>
    );
};

export default NewComponent;
