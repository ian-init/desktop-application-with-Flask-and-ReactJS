import React, { useState, useEffect } from 'react';


import c from "../../../backend/graph_plot.png"


const NewComponent = () => {
    const [length, setLength] = useState(null); // State to store the length
    const [density, setDensity] = useState(null);  // State to hold the length of the dataframe
    const [columns, setColumns] = useState([]);  // State to hold the column names

    // Fetch the length from the backend when the component mounts
    useEffect(() => {
        const fetchResult = async () => {
            try {
                const response = await fetch(`http://localhost:5000/get-result`); // Make sure this endpoint returns the length
                const result = await response.json();

                if (response.ok) {
                    setLength(result.length); // Set the length received from the backend
                    setDensity(result.Density)
                    setColumns(result.columns)
                    console.log(columns)
                    console.log(density)
                } else {
                    console.error("Error:", result.error);
                }
            } catch (error) {
                console.error("Error:", error);
            }
        };
        fetchResult();
    }, []);  // Add an empty array as the second argument to only run once

    return (
        <>
        <div>
            <h1>Node details</h1>
            {length !== null ? (
                <div>
                    <h2>File Length: {length}</h2>
                    <h2>Den: {density}</h2>
                    <h2>Den: {columns.join(', ')}</h2>
                </div>
            ) : (
                <p>Loading file length...</p>
            )}
        </div>
        <div>
            <img src={c} alt="Graph Visualization" />
        </div>
        </>
    );
};

export default NewComponent;