import React, { useState } from 'react';
import './viewUploadResult.css'

function Snowball() {
    // State to hold form data
    const [startNodeAndCycle, setStartNodeAndCycle] = useState({
        startNode: '',
        numCycle: ''
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    // State for fetched data
    const [length, setLength] = useState(null);
    const [density, setDensity] = useState(null);
    const [averageClustering, setAverageClustering] = useState(null);
    const [nodesNum, setNodesNum] = useState(null);
    const [edgesNum, setEdgesNum] = useState(null);
    const [transitivity, setTransitivity] = useState(null); 
    const [columns, setColumns] = useState([]);
    const [image, setImage] = useState('');

    // Handler to manage form input changes
    const handleChange = (event) => {
        const { name, value } = event.target;
        setStartNodeAndCycle(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    // Form submit handler to send data to the backend and update the frontend
    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5000/get-snowball', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(startNodeAndCycle),
            });
            const result = await response.json(); // Fetch the returned JSON data

            if (response.ok) {
                // Update state with the fetched data
                setLength(result.length);
                setDensity(result.Density);
                setColumns(result.columns);
                setAverageClustering(result.Averageclustering);
                setNodesNum(result.NodesNum);
                setEdgesNum(result.EdgesNum);
                setTransitivity(result.Transitivity);
                setImage(`data:image/png;base64,${result.image}`);
                setError(null); // Clear any previous errors
            } else {
                console.error("Error:", result.error);
                setError("Failed to fetch node statistics.");
            }
        } catch (error) {
            console.error("Error sending data to backend:", error);
            setError('Failed to submit form data.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
        <h1>Generate snowball subset from uploaded edge network</h1>
            
        <div className='grid'>

            <form style={{margin: 'auto'}}onSubmit={handleSubmit}>
                <label htmlFor="startNode">Start node:</label>
                <input
                    type="text"
                    id="startNode"
                    name="startNode"
                    value={startNodeAndCycle.startNode}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="numCycle">Number of cycles:</label>
                <input
                    type="text"
                    id="numCycle"
                    name="numCycle"
                    value={startNodeAndCycle.numCycle}
                    onChange={handleChange}
                    required
                />

                <button type="submit">Submit</button>
                {loading && <p>Loading...</p>}
                {error && <p>{error}</p>}
            </form>
        </div>
            {/* Display fetched node statistics */}
            {length !== null && (
                <div className='grid'>
            <div className='container'>
                    <h2>Snowball subset analysis</h2>
                    <p>No. of rows in the subset: {length}</p>
                    <p>Columns: {columns.join(', ')}</p>
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
                                <td>{averageClustering}</td>
                            </tr>
                            <tr>
                                <td>Transitivity</td>
                                <td>{transitivity}</td>
                            </tr>
                    </table>
                </div>
                <div className='container'>
                    {image && <img style={{height: "60vh"}} src={image} alt="Node Visualization" />}
                    </div>
                </div>
            )}
       
        </>
    );
}

export default Snowball;