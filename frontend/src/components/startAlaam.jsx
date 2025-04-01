import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';

function startAlaam() {
    const [attributeDict, setAttributeDict] = useState({});
    const [selectedAttribute, setSelectedAttribute] = useState('');
    const [maxRuns, setMaxRuns] = useState('');
    const [numSubphases, setNumSubphases] = useState('');
    const [phase3steps, setPhase3steps] = useState('');

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    const [alaamResults, setAlaamResults] = useState([]);
    const [networkType, setNetworkType] = useState("");

    // fetch attribute list of dataset 
    useEffect(() => {
        const fetchResult = async () => {
            try {
                const response = await fetch('http://localhost:5000/get-attributevisualisation');
                const result = await response.json();
    
                if (response.ok) {
                    setAttributeDict(result.attributeDict);
                    setLoading(false);
                } else {
                    console.error("Error:", result.error);
                }
            } catch (error) {
                console.error("Error:", error);
                setError(error);
                setLoading(false);
            }
        };
        fetchResult();
        // import html2pdf
        const script = document.createElement('script');
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.3/html2pdf.bundle.min.js";
        script.async = true;
        document.body.appendChild(script);
        // Cleanup function to remove the script when the component unmounts
        return () => {
            document.body.removeChild(script);
        };
    }, []);

    const handleDownloadPDF = () => {
        const element = document.getElementById('report-content');
        html2pdf()
        .set({
            margin: 10, 
            filename: 'alaam_report.pdf',
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

    // handle form value and submission
    const handleSubmit = (event) => {
        event.preventDefault();
        fetch('http://localhost:5000/get-startAlaam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selectedAttribute: selectedAttribute, maxRuns: maxRuns, numSubphases: numSubphases, phase3steps: phase3steps }),
        })
        .then(response => response.json())
        .then(data => {
            setAlaamResults(data); // Store the results in the alaamResults state
            if (data.length > 0) {
                setNetworkType(data[0].network_type);
            }
        })
        .catch(error => console.error('Error sending data to backend:', error));
    };
    const handleSelectChange = (event) => {
        const { name, value } = event.target;
    
        if (name === 'selectedAttribute') {
            setSelectedAttribute(value);
        } else if (name === 'maxRuns') {
            setMaxRuns(value);
        } else if (name === 'numSubphases') {
            setNumSubphases(value);
        } else if (name === 'phase3steps') {
            setPhase3steps(value);
        }
    };
    
    const navigate = useNavigate();
    const handleNavigateToERGM = () => {
        navigate('/ergm');
    };

    if (loading) {
        return <div>Loading...</div>;
    }
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <>
        <h1>ALAAMEE Stochastic Approximation</h1>
        <div className='grid'>
            <div className='container'>    
            <form style={{ margin: 'auto' }} onSubmit={handleSubmit}>
                <label>Select one attribute for ALAAM:</label>
                <select name="selectedAttribute" onChange={handleSelectChange} value={selectedAttribute}>
                    <option value="" disabled>Select an attribute</option>
                    {Object.keys(attributeDict).map((key) => (
                    <option key={key} value={key}>
                        {key}
                    </option>
                ))}
                </select>
                <br></br>
                <label htmlFor="maxRuns">Max. estimation runs:</label>
                <input
                    type="text"
                    id="maxRuns"
                    name="maxRuns"
                    value={maxRuns}
                    onChange={handleSelectChange}
                    required/>
                <br></br>
                <label htmlFor="numSubphases">Subphases:</label>
                <input
                    type="text"
                    id="numSubphases"
                    name="numSubphases"
                    value={numSubphases}
                    onChange={handleSelectChange}
                    required/>
                <br></br>
                <label htmlFor="phase3steps">Iterations in phase 3:</label>
                <input
                    type="text"
                    id="phase3steps"
                    name="phase3steps"
                    value={phase3steps}
                    onChange={handleSelectChange}
                    required/>                          
                <button type="submit">Submit</button>
            </form>
            <br></br>
            <br></br>
                
            {alaamResults.length > 0 && (
                <div id='report-content'>
                    {networkType && <h3>Network Type: {networkType}</h3>}
                    <div className='container'>
                   
                        <table className='table'>
                            <thead>
                                <tr>
                                <th>Effect</th>
                                <th>Lambda</th>
                                <th>Parameter</th>
                                <th>StdErr</th>
                                <th>T-Ratio</th>
                                <th>SACF</th>
                                <th>Param/StdErr</th>
                                </tr>
                            </thead>
                            <tbody>
                                {alaamResults.map((result, index) => {
                                const paramStdErrRatio = result.parameter / result.stderr;
                                const tratio = result.t_ratio;
                                return (
                                    <tr key={index}>
                                        <td>{result.effect}</td>
                                        <td>{result.lambda}</td>
                                        <td>{result.parameter}</td>
                                        <td>{result.stderr}</td>
                                        <td className={tratio < 0.1 ? 'alaamhighlight2' : ''}>{result.t_ratio}</td>
                                        <td>{result.sacf}</td>
                                        <td className={paramStdErrRatio > 2 ? 'alaamhighlight1' : ''}>{paramStdErrRatio.toFixed(3)}</td>
                                    </tr>
                                );
                                })}
                            </tbody>
                        </table>
                        <p style={{color: 'rgb(109, 109, 255'}}>A ratio of parameter estimate over standard error &#62;2 indicates the paramet is significant</p>
                        <p style={{color: 'rgb(109, 109, 255)'}}>Less than 0.1 t-ratio indicates estimatation has converged</p>
                        <br></br>
                    </div>
                </div>
            )}
            {alaamResults.length > 0 && (
                <div style={{ display: "flex", justifyContent: "space-evenly", margin: '30px'}}>
                    <button onClick={handleDownloadPDF}>Download Report</button>
                    <button onClick={handleNavigateToERGM}>ERGM analysis</button>
                </div>
            )}
            </div>
        </div>
        </>
    );
}

export default startAlaam;