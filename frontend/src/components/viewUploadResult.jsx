import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import React, { useState } from 'react';

import AttributeDescriptiveStat from './attributeDescriptiveStat.jsx'
import NodeDescriptiveStat from './nodeDescriptiveStat.jsx'

const viewUploadResult = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/startAlaam');
  };
    return (
    <>
      <AttributeDescriptiveStat />
      <NodeDescriptiveStat />
      <button onClick={handleButtonClick}>Start Alaam</button>  
    </>
  )
}
export default viewUploadResult;