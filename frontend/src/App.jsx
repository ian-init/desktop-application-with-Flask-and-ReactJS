import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import React, { useState } from 'react';

import FileUpload from './components/fileUpload.jsx'
import ViewUploadResult from './components/viewUploadResult.jsx'
import StartAlaam from './components/startAlaam.jsx';
import Snowball from './components/snowball.jsx';

import './App.css';
import '../src/components/viewUploadResult.css'

const FileUploadModule = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/viewUploadResult'); // Navigate to the 2nd component route
  };
  return (
    <div>
    <FileUpload
      htmlTitle={"Attribute list"}
      flaskHost={"http://localhost:5000/upload"}
    />
    <FileUpload
      htmlTitle={"Edge list"}
      flaskHost={"http://localhost:5000/upload_2"}
    />
    <hr></hr>
      <button style={{margin: '30px'}}onClick={handleButtonClick}>Confirm upload</button>
    </div>
  );
};

function App() {
  const [showSecond, setShowSecond] = useState(false);

  const handleButtonClick = () => {
    setShowSecond(!showSecond); // Toggle the display of the 2nd component
  };
  return (
	<>
    <Router>
      <Routes>
        <Route path="/" element={<FileUploadModule />} />
        <Route path="/viewUploadResult" element={<ViewUploadResult />} />
        <Route path="/startAlaam" element={<StartAlaam />} />
        <Route path="/snowball" element={<Snowball />} />
      </Routes>
    </Router>
	</>
  )
}
export default App;