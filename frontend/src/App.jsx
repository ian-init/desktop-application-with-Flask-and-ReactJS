import './App.css';
import FileUpload from './components/fileUpload.jsx'
import View from './components/viewUploadResult.jsx'
import React, { useState } from 'react';

import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';


const MainComponent = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/second'); // Navigate to the 2nd component route
  };

  return (
    <div>
    <FileUpload
        htmlTitle={"Attribute list"}
        flaskHost={"http://localhost:5000/upload"}
    />
    <FileUpload
      htmlTitle={"Nodes list"}
      flaskHost={"http://localhost:5000/upload_2"}
    />
      <button onClick={handleButtonClick}>
        Open 2nd Component
      </button>
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
        <Route path="/" element={<MainComponent />} />
        <Route path="/second" element={<View />} />
      </Routes>
    </Router>
	</>
  )
}
export default App;