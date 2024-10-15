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
  const handleNavigateToSnowball = () => {
    navigate('/snowball');
  };

  return (
    <>
      <AttributeDescriptiveStat />
      <NodeDescriptiveStat />
      <NetworkXCentrality setCentrality={setCentrality} /> 
      <hr></hr>
      <div style={{ display: "flex", justifyContent: "space-evenly", margin: '30px'}}>
        <button onClick={handleNavigateToSnowball} >Snowball sampling</button>
        <button onClick={handleNavigateToAlaam} >Initiate Alaam</button>
      </div>
    </>
  );
}

export default viewUploadResult;