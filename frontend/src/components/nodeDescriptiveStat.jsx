import React, { useState, useEffect } from 'react';
import './viewUploadResult.css'

const NodeDescriptiveStat = () => {
    const [length, setLength] = useState(null);
    const [density, setDensity] = useState(null);
    const [averageclustering, setAverageclustering] = useState(null);
    const [nodesNum, setNodesNum] = useState(null);
    const [edgesNum, setEdgesNum] = useState(null);
    const [clusteringcoefficient, setClusteringCoefficient] = useState(null); 
    const [transitivity, setTransitivity] = useState(null); 
    const [columns, setColumns] = useState([]);
    const [image, setImage] = useState('');

    // Fetch the json from backend when the component mounts
    useEffect(() => {
        const fetchResult = async () => {
            try {
                const response = await fetch(`http://localhost:5000/get-nodedescriptivestat`); // Make sure this endpoint returns the length
                const result = await response.json();

                if (response.ok) {
                    setLength(result.length); // Set the length received from the backend
                    setDensity(result.Density)
                    setColumns(result.columns)
                    setAverageclustering(result.Averageclustering)
                    setNodesNum(result.NodesNum)
                    setEdgesNum(result.EdgesMum)
                    setClusteringCoefficient(result.ClusteringCoefficient)
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
                <h1>Node details</h1>
                {length !== null ? (
                    <div>
                        <p>No. of row in file: {length}</p>
                        <p>Column Name: {columns.join(', ')}</p>
                        <table className='table'>
                            <tr>
                                <th>Measurement</th>
                                <th>Value</th>
                            </tr>
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
                                <td>Clustering Coefficient</td>
                                <td>{clusteringcoefficient}</td>
                            </tr>
                            <tr>
                                <td>Transitivity</td>
                                <td>{transitivity}</td>
                            </tr>
                        </table>
                   
                    </div>
                ) : (
                    <p>No file uploaded, please retry...</p>
                )}
            </div>
            <div className='container'>
                {image && <img style={{height: "60vh"}} src={image} alt="Node Visualization" />}
            </div>
        </div>
        </>
    );
};

export default NodeDescriptiveStat;