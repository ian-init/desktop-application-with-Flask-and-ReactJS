import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import './App.css';
import FileUpload from './components/fileUpload.jsx'
import ViewUploadResult from './components/viewUploadResult.jsx'
import React, { useState } from 'react';

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
      htmlTitle={"Nodes list"}
      flaskHost={"http://localhost:5000/upload_2"}
    />
      <button onClick={handleButtonClick}>Confirm upload</button>
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
      </Routes>
    </Router>
	</>
  )
}
export default App;