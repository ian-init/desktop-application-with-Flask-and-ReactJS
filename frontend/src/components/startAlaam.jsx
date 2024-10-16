import React, { useEffect, useState } from 'react';

function startAlaam() {
    const [attributeDict, setAttributeDict] = useState({});
    const [selectedAttribute, setSelectedAttribute] = useState('');

    const [maxRuns, setMaxRuns] = useState('');
    const [numSubphases, setNumSubphases] = useState('');
    const [phase3steps, setPhase3steps] = useState('');

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [alaamResults, setAlaamResults] = useState([]);

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
    }, []);

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('Submitting attribute:', selectedAttribute);
        fetch('http://localhost:5000/get-startAlaam', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selectedAttribute: selectedAttribute, maxRuns: maxRuns, numSubphases: numSubphases, phase3steps: phase3steps }), // Send the selected attribute
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response from Flask:', data);
            setAlaamResults(data); // Store the results in the alaamResults state
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
                <label htmlFor="maxRuns">Max. estimation runs:</label>
                <input
                    type="text"
                    id="maxRuns"
                    name="maxRuns"
                    value={maxRuns}
                    onChange={handleSelectChange}
                    required/>
                <label htmlFor="numSubphases">Subphases:</label>
                <input
                    type="text"
                    id="numSubphases"
                    name="numSubphases"
                    value={numSubphases}
                    onChange={handleSelectChange}
                    required/>
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
                        <th>Param/StdErr</th> {/* New column */}
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
                                <td className={paramStdErrRatio > 2 ? 'alaamhighlight1' : ''}>{paramStdErrRatio.toFixed(3)}</td> {/* Conditionally applying the CSS class for Param/StdErr Ratio */}
                            </tr>
                        );
                        })}
                    </tbody>
                </table>
                <p style={{color: 'rgb(109, 109, 255'}}>2x parameter estimate than standard error indicates the paramet is significant</p>
                <p style={{color: 'rgb(255, 119, 119)'}}>Less than 0.1 t-ratio indicates estimatation hasconverged</p>
            </div>
            )}
            </div>
        </div>
        </>
    );

}

export default startAlaam;