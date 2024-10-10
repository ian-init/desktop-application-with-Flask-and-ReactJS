import React, { useState, useEffect } from 'react';
import './viewUploadResult.css'
import a from "../../../backend/pie_chart.png"

const AttributeDescriptiveStat = () => {
  const [attributeDict, setAttributeDict] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch the dictionary from backend when the component mounts
  useEffect(() => {
    const fetchResult = async () => {
        try {
            const response = await fetch('http://localhost:5000/get-attributevisualisation');
            const result = await response.json();

            if (response.ok) {
                setAttributeDict(result);  // Use 'result' here
                setLoading(false);
            } else {
                console.error("Error:", result.error);
            }
        } catch (error) {
            console.error("Error:", error);
            setError(error);
            setLoading(false);  // Set loading to false when there is an error
        }
    };
    fetchResult();
  }, []);  // Empty array ensures this effect runs only once

  // Show loading state
  if (loading) {
    return <div>Loading...</div>;
  }

  // Show error if any
  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <>
    <div className='grid'>
        <div className='container'>
        <h1>Attribute Dictionary Table</h1>
        <table border="1">
            <thead>
            <tr>
                <th>Column Name</th>
                <th>Unique Values</th>
            </tr>
            </thead>
            <tbody>
            {Object.keys(attributeDict).map((columnName, index) => (
                <tr key={index}>
                <td>{columnName}</td>
                <td>{Array.isArray(attributeDict[columnName]) ? attributeDict[columnName].join(', ') : attributeDict[columnName]}</td>
                {/* Ensure the values are joined into a string */}
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    </div>
    
    <div className='grid'>
        <div className='container'>
            <img src={a} alt="Graph Visualization" />
        </div>
        <div className='container'>
            <img src={a} alt="Graph Visualization" />
        </div>
        <div className='container'>
            <img src={a} alt="Graph Visualization" />
        </div>
    </div>
    
    <div className='grid'>
        <div className='container'>
            <img src={a} alt="Graph Visualization" />
        </div>
        <div className='container'>
            <img src={a} alt="Graph Visualization" />
        </div>
        <div className='container'>
            <img src={a} alt="Graph Visualization" />
        </div>
    </div>
    
   
    </>
  );
};

export default AttributeDescriptiveStat;
