import React, { useState, useEffect } from 'react';

const NodeDescriptiveStat = () => {
    const [length, setLength] = useState(null);
    const [density, setDensity] = useState(null);
    const [averageclustering, setAverageclustering] = useState(null);
    const [nodesNum, setNodesNum] = useState(null);
    const [edgesNum, setEdgesNum] = useState(null);
    const [transitivity, setTransitivity] = useState(null); 
    const [columns, setColumns] = useState([]);
    const [image, setImage] = useState('');

    // Fetch json format dictionary
    useEffect(() => {
        const fetchResult = async () => {
            try {
                const response = await fetch(`http://localhost:5000/get-nodedescriptivestat`);
                const result = await response.json();

                if (response.ok) {
                    setLength(result.length);
                    setDensity(result.Density)
                    setColumns(result.columns)
                    setAverageclustering(result.Averageclustering)
                    setNodesNum(result.NodesNum)
                    setEdgesNum(result.EdgesNum)
                    setTransitivity(result.Transitivity)
                    setImage(`data:image/png;base64,${result.image}`);
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
        <div className='grid'>
            <div className='container'>
                <h1>Edge analysis</h1>
                {length !== null ? (
                    <div>
                        <p>No. of row in file: {length}</p>
                        <p>Column Name: {columns.join(', ')}</p>
                        <table className='table'>
                            <thead>
                                <tr>
                                    <th>Measurement</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                            <tr>
                                <td>Number of Nodes</td>
                                <td>{nodesNum}</td>
                            </tr>
                            <tr>
                                <td>Number of Edges</td>
                                <td>{edgesNum}</td>
                            </tr>
                            <tr>
                                <td>Density</td>
                                <td>{density}</td>
                            </tr>
                            <tr>
                                <td>Average Clustering</td>
                                <td>{averageclustering}</td>
                            </tr>
                            <tr>
                                <td>Transitivity</td>
                                <td>{transitivity}</td>
                            </tr>
                            </tbody>
                        </table>
                   
                    </div>
                ) : (
                    <p>No file uploaded, please retry...</p>
                )}
            </div>
            <div className='container'>
                {image && <img style={{height: '100%'}}src={image} alt="Edge Visualization" />}
            </div>
        </div>
        </>
    );
};

export default NodeDescriptiveStat;