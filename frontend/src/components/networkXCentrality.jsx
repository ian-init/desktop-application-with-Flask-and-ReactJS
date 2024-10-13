import React, { useState } from 'react';

function CentralityForm({ setCentrality }) {
  const [localCentrality, setLocalCentrality] = useState(''); // Local state to store centrality

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
    console.log('Response from Flask:', data);
  };

  return (
    <form onSubmit={handleSubmitToFlask}>
      <label>Select a centrality Measurement:</label>
      <select onChange={handleSelectChange} value={localCentrality}>
        <option value="1">Betweenness</option>
        <option value="2">Closeness</option>
        <option value="3">Eigenvector</option>
        <option value="4">Clustering Coefficient</option>
      </select>
      <button type="submit">Submit to Flask</button>
    </form>
  );
}

export default CentralityForm;
