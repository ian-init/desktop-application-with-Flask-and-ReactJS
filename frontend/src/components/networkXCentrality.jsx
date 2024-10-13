import React, { useState, useEffect } from 'react';

function CentralityForm({ setCentrality }) {
  const [localCentrality, setLocalCentrality] = useState(''); // Local state to store centrality
  const [image, setImage] = useState('');

  const handleSelectChange = (event) => {
    const selectedValue = event.target.value;
    setLocalCentrality(selectedValue); // Update local state
    setCentrality(selectedValue); // Update the parent component's state
  };

  const handleSubmitToFlask = async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page

    // Send the selected centrality value to Flask backend
    const response = await fetch('http://localhost:5000/get-centrality', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ centrality: localCentrality }),
    });

    const data = await response.json();
    // Set the base64 image string from Flask response into the state
    setImage(`data:image/png;base64,${data.image}`);
  };

  return (
    <div>
    <form onSubmit={handleSubmitToFlask}>
      <label>Select a centrality Measurement:</label>
      <select onChange={handleSelectChange} value={localCentrality}>
        <option value="Betweenness">Betweenness</option>
        <option value="Closeness">Closeness</option>
        <option value="Eigenvector">Eigenvector</option>
        <option value="ClusteringCoefficient">Clustering Coefficient</option>
      </select>
      <button type="submit">Submit to Flask</button>
    </form>
    {image && <img src={image} alt="Edge Histogram" />}
    </div>
  );
}

export default CentralityForm;
