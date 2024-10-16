import React, { useState } from 'react';

function CentralityForm({ setCentrality }) {
  const [localCentrality, setLocalCentrality] = useState('');
  const [binSize, setBinSize] = useState('');
  const [image, setImage] = useState('');

  const handleSelectChange = (event) => {
    const { name, value } = event.target;

    if (name === 'localCentrality') {
      setLocalCentrality(value); // Update state for localCentrality
      setCentrality(value); // Update the parent component's state if needed
    } else if (name === 'binSize') {
      setBinSize(value); // Update state for binSize
    }
  };

  const handleSubmitToFlask = async (event) => {
    event.preventDefault(); // Prevent form from reloading the page

    const response = await fetch('http://localhost:5000/get-centrality', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ centrality: localCentrality, binSize: binSize }),
    });

    const data = await response.json();
    setImage(`data:image/png;base64,${data.image}`);
  };

  return (
    <>
    <h1>Centrality analysis</h1>
    <div className='grid'>
      <div className='container'>
      <form onSubmit={handleSubmitToFlask}>
        <label>Select a centrality Measurement:</label>
        <select
          name="localCentrality"
          onChange={handleSelectChange}
          value={localCentrality}>
          <option value="">Please Select</option>
          <option value="Betweenness">Betweenness</option>
          <option value="Closeness">Closeness</option>
          <option value="Eigenvector">Eigenvector</option>
          <option value="ClusteringCoefficient">Clustering Coefficient</option>
        </select>
        <br></br>
        <label htmlFor="binSize">Select a bin size:</label>
        <input
          type="text"
          id="binSize"
          name="binSize"
          value={binSize}
          onChange={handleSelectChange}
          required/>

        <button type="submit">Generate</button>
        {image !== '' && (
          <p style={{color: "#FF0000"}}>Histogram already saved in export folder</p>
        )}
      </form>


      </div>
      {image !== '' && (
      <div className='container'>
      {image && <img src={image} alt="Edge Histogram" />}
      </div>
      )}
    </div>
    </>
  );
}

export default CentralityForm;
