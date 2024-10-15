import React, { useEffect, useState } from 'react';
import './viewUploadResult.css'

function startAlaam() {
    const [attributeDict, setAttributeDict] = useState({});
    const [selectedAttributes, setSelectedAttributes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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
            // Handle the response from the backend if needed
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
                <form onSubmit={handleSubmit}>
                    {Object.keys(attributeDict).map((key) => (
                        <div key={key}>
                            <input 
                                type="checkbox" 
                                id={key} 
                                name={key} 
                                onChange={handleCheckboxChange} 
                            />
                            <label htmlFor={key}>{key}</label>
                        </div>
                    ))}
                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
    }

export default startAlaam;