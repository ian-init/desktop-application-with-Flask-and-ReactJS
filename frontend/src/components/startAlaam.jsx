import React, { useEffect, useState } from 'react';
import './viewUploadResult.css'

function startAlaam() {
    const [attributeDict, setAttributeDict] = useState({});
    const [selectedAttributes, setSelectedAttributes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [alaamResults, setAlaamResults] = useState([]); // New state variable for storing results

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
        fetch('http://localhost:5000/get-alaamVariables', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selectedAttributes }), // Send the selectedAttributes state variable
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response from Flask:', data);
            setAlaamResults(data); // Store the results in the alaamResults state
        })
        .catch(error => console.error('Error sending data to backend:', error));
    }

    const handleCheckboxChange = (event) => {
        const attribute = event.target.name;
        if (event.target.checked) {
            setSelectedAttributes([...selectedAttributes, attribute]);
        } else {
            setSelectedAttributes(selectedAttributes.filter(attr => attr !== attribute));
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div className='grid'>
            <div className='container'>
                <form style={{margin: 'auto'}} onSubmit={handleSubmit}>
                    <label>Select one attribute for ALAAM:</label>
                    <select onChange={handleCheckboxChange}>
                        {Object.keys(attributeDict).map((key) => (
                            <option key={key} value={key}>
                                {key}
                            </option>
                        ))}
                    </select>
                    <button type="submit">Submit</button>
                </form>

                {/* Render the results table if alaamResults is not empty */}
                {alaamResults.length > 0 && (
                    <table className='table'>
                        <thead>
                            <tr>
                                <th>Effect</th>
                                <th>Lambda</th>
                                <th>Parameter</th>
                                <th>StdErr</th>
                                <th>T-Ratio</th>
                                <th>SACF</th>
                            </tr>
                        </thead>
                        <tbody>
                            {alaamResults.map((result, index) => (
                                <tr key={index}>
                                    <td>{result.effect}</td>
                                    <td>{result.lambda}</td>
                                    <td>{result.parameter}</td>
                                    <td>{result.stderr}</td>
                                    <td>{result.t_ratio}</td>
                                    <td>{result.sacf}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}

export default startAlaam;