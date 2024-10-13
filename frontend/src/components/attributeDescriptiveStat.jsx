import React, { useState, useEffect } from 'react';
import './viewUploadResult.css'

const AttributeDescriptiveStat = () => {
  const [attributeDict, setAttributeDict] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [image, setImage] = useState('');
  const [length, setLength] = useState(null);
  const [columns, setColumns] = useState([]);

  // Fetch the dictionary from backend when the component mounts
  useEffect(() => {
    const fetchResult = async () => {
        try {
            const response = await fetch('http://localhost:5000/get-attributevisualisation');
            const result = await response.json();

            if (response.ok) {
                setLength(result.length);
                setColumns(result.columns)
                setAttributeDict(result.attributeDict);
                setImage(`data:image/png;base64,${result.image}`);
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
        <p>No. of row in file: {length}</p>
        <p>Column Name: {columns.join(', ')}</p>
        <table className='table'>
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
        <div className='container'>
                {image && <img style={{height: "60vh"}} src={image} alt="Node Visualization" />}
        </div>
    </div>  
   
    </>
  );
};

export default AttributeDescriptiveStat;
