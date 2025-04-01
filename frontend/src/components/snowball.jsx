import React, { useState, useEffect } from 'react'; 
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';

function Snowball() {
    const [startNodeAndCycle, setStartNodeAndCycle] = useState({
        startNode: '',
        numCycle: ''
    });

    const [length, setLength] = useState(null);
    const [density, setDensity] = useState(null);
    const [averageClustering, setAverageClustering] = useState(null);
    const [nodesNum, setNodesNum] = useState(null);
    const [edgesNum, setEdgesNum] = useState(null);
    const [transitivity, setTransitivity] = useState(null); 
    const [columns, setColumns] = useState([]);
    const [image, setImage] = useState('');

    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    // Handler to manage form input changes
    const handleChange = (event) => {
        const { name, value } = event.target;
        setStartNodeAndCycle(prevState => ({
            ...prevState,
            [name]: value
        }));
    };
    
    const navigate = useNavigate();
    const handleNavigateToAlaam = () => {
        navigate('/startSnowballAlaam');
      };

    // import html2pdf
    useEffect(() => {
        const script = document.createElement('script');
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.3/html2pdf.bundle.min.js";
        script.async = true;
        document.body.appendChild(script);

        return () => {
            document.body.removeChild(script);
        };
    }, []);

    const handleDownloadPDF = () => {
        const element = document.getElementById('report-content');
        html2pdf()
        .set({
            margin: 1, 
            filename: 'snowball_report.pdf',
            image: { type: 'jpeg', quality: 1 },  // Set image quality
            html2canvas: {
                scale: 5,  // Increase scale for better resolution
                logging: true,
            },
            jsPDF: {
                unit: 'pt',  // Unit in points (1/72 of an inch)
                format: 'a4',  // Set format to A4
                orientation: 'portrait',  // Orientation of the PDF
            }
        })
        .from(element)
        .save();
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
            const result = await response.json();

            if (response.ok) {
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
            <form style={{margin: 'auto'}} onSubmit={handleSubmit}>
                <label htmlFor="startNode">Start node:</label>
                <input
                    type="text"
                    id="startNode"
                    name="startNode"
                    value={startNodeAndCycle.startNode}
                    onChange={handleChange}
                    required
                />
                <br></br>
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
        <div id="report-content">
                {length !== null && (
                <div className='grid'>
                    <div className='container'>
                        <h2>Snowball subset analysis</h2>
                        <p>No. of rows in the subset: {length}</p>
                        <p>Columns: {columns.join(', ')}</p>
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
                                    <td>{averageClustering}</td>
                                </tr>
                                <tr>
                                    <td>Transitivity</td>
                                    <td>{transitivity}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div className='container'>
                        {image && <img src={image} alt="Node Visualization" />}
                    </div>       
                </div>    
                )}
        </div>
        {length !== null && (
        <p style={{color: "#FF0000"}}>The clustered network is already saved in to export folder</p>
        )}
        <hr></hr>
        {length !== null && (
        <div style={{ display: "flex", justifyContent: "space-evenly", margin: '30px'}}>
            <button onClick={handleDownloadPDF}>Download File</button>
            <button onClick={handleNavigateToAlaam} >Initiate Alaam</button>
        </div>
        )}
        </>
    );
}

export default Snowball;