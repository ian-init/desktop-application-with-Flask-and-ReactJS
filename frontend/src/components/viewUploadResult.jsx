import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';

import AttributeDescriptiveStat from './attributeDescriptiveStat.jsx'
import NodeDescriptiveStat from './nodeDescriptiveStat.jsx'
import NetworkXCentrality from './networkXCentrality.jsx'

const viewUploadResult = () => {
  const navigate = useNavigate();
  const [centrality, setCentrality] = useState('');

  // Function to navigate to the /startAlaam route
  const handleNavigateToAlaam = () => {
    navigate('/startAlaam');
  };

  return (
    <>
      <AttributeDescriptiveStat />
      <NodeDescriptiveStat />
      
      {/* Pass setCentrality to CentralityForm to keep track of the centrality value */}
      <NetworkXCentrality setCentrality={setCentrality} />  
      {/* Button to navigate to /startAlaam */}
      <button onClick={handleNavigateToAlaam}>Start Alaam</button>
    </>
  );
}

export default viewUploadResult;