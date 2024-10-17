import React, { useState, useEffect } from 'react'; 
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';

import AttributeDescriptiveStat from './attributeDescriptiveStat.jsx'
import NodeDescriptiveStat from './nodeDescriptiveStat.jsx'
import NetworkXCentrality from './networkXCentrality.jsx'

import '../index.css'

function viewUploadResult() {
  const navigate = useNavigate();
  const [centrality, setCentrality] = useState('');

  const handleNavigateToAlaam = () => {
    navigate('/startAlaam');
  };
  const handleNavigateToSnowball = () => {
    navigate('/snowball');
  };

  useEffect(() => {
    const script = document.createElement('script');
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.3/html2pdf.bundle.min.js";
    script.async = true;
    document.body.appendChild(script);

    return () => {
        document.body.removeChild(script);
    };
  }, []);

  const handleDownloadDescriptiveStat = () => {
    const element = document.getElementById('descriptive_stat');
    html2pdf()
    .set({
      margin: 1, 
      filename: 'descriptive_stat.pdf',
      image: { type: 'jpeg', quality: 1 },  // Set image quality
      html2canvas: {
      scale: 5,  // Increase scale for better resolution
      logging: true,

      },
      jsPDF: {
        unit: 'pt',  // Unit in points (1/72 of an inch)
        format: 'a4',  // Set format to A4
        orientation: 'portrait',  // Orientation of the PDF
        putTotalPages: 'true',
      }
    })
    .from(element)
    .save();
    };

  return (
    <>
    <div id='descriptive_stat'>
      <AttributeDescriptiveStat />
      <div className="html2pdf__page-break"></div>
      <NodeDescriptiveStat />
    </div>
      <button onClick={handleDownloadDescriptiveStat}>Download report</button>
      <br></br>
      <br></br>
      <hr></hr>
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