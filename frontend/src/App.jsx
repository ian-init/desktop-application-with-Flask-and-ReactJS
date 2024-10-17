import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import React, { useState } from 'react';

import FileUpload from './components/fileUpload.jsx'
import ViewUploadResult from './components/viewUploadResult.jsx'
import StartAlaam from './components/startAlaam.jsx';
import Snowball from './components/snowball.jsx';
import SnowballAlaam from './components/startSnowballAlaam.jsx';
import ERGM from './components/ergm.jsx'

const FileUploadModule = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/viewUploadResult'); // Navigate to the 2nd component route
  };
  return (
    <>
    <div className='grid'>
      <FileUpload
        htmlTitle={"Attribute list"}
        flaskHost={"http://localhost:5000/upload"}
      />
      <hr></hr>
      <FileUpload
        htmlTitle={"Edge list"}
        flaskHost={"http://localhost:5000/upload_2"}
      />
    </div>
    <hr></hr>
    <div>
      <button style={{margin: '30px'}}onClick={handleButtonClick}>Confirm upload</button>
    </div>
    </>
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
        <Route path="/startSnowballAlaam" element={<SnowballAlaam />} />
        <Route path="/ergm" element={<ERGM />} />
      </Routes>
    </Router>
	</>
  )
}
export default App;