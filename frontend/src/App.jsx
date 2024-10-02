import { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [length, setLength] = useState(null);  // State to hold the length of the dataframe

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('Please select a file first.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      // Check if the response is OK and properly defined
      if (!response.ok) {
        const errorData = await response.json();
        setMessage(errorData.error || 'An error occurred');
      } else {
        const data = await response.json();  // Make sure to await the response.json
        setMessage('File uploaded successfully');
        setLength(data.length);  // Update the length state with the value from the backend
      }
    } catch (error) {
      setMessage('An error occurred while uploading the file.');
      console.error(error);
    }
  };

  return (
    <>
      <div>
        <h1>{message}</h1>
        <h2>File Upload Form</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload File</button>
        <p>{length !== null ? `Length of CSV: ${length}` : 'No data uploaded yet'}</p>  {/* Display length */}
      </div>
    </>
  );
}

export default App;
