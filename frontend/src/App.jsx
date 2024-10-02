import { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [length, setLength] = useState(null);  // State to hold the length of the dataframe
  const [columns, setColumns] = useState([]);  // State to hold the column names

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

      if (!response.ok) {
        const errorData = await response.json();
        setMessage(errorData.error || 'An error occurred');
      } else {
        const data = await response.json();
        setMessage('File uploaded successfully');
        setLength(data.length);
        setColumns(data.columns);
      }
    } catch (error) {
      setMessage('An error occurred while uploading the file.');
      console.error(error);
    }
  };

  // Second file upload logic
  const [selectedFile_2, setSelectedFile_2] = useState(null);
  const [message_2, setMessage_2] = useState('');
  const [length_2, setLength_2] = useState(null);  // State to hold the length of the second dataframe
  const [columns_2, setColumns_2] = useState([]);  // State to hold the column names for the second file

  const handleFileChange_2 = (event_2) => {
    setSelectedFile_2(event_2.target.files[0]);
  };

  const handleUpload_2 = async () => {
    if (!selectedFile_2) {
      setMessage_2('Please select a file first.');
      return;
    }

    const formData_2 = new FormData();
    formData_2.append('file', selectedFile_2);

    try {
      const response_2 = await fetch('http://localhost:5000/upload_2', {  // Assuming a different endpoint for the second file
        method: 'POST',
        body: formData_2,
      });

      if (!response_2.ok) {
        const errorData_2 = await response_2.json();
        setMessage_2(errorData_2.error || 'An error occurred');
      } else {
        const data_2 = await response_2.json();
        setMessage_2('File uploaded successfully');
        setLength_2(data_2.length);
        setColumns_2(data_2.columns);
      }
    } catch (error_2) {
      setMessage_2('An error occurred while uploading the file.');
      console.error(error_2);
    }
  };

  return (
    <>

      <div>
        <h1>First File Upload Form</h1>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload First File</button>
        <p>{message}</p>
        {columns.length > 0 && (
          <div>
            <p>{length !== null ? `Length of CSV: ${length}` : 'No data uploaded yet'}</p>
          </div>
        )}
        {columns.length > 0 && (
          <div>
            <p>Column Names: {columns.map((col, index) => (
              <span key={index}> {col}{index < columns.length - 1 ? ', ' : ''}</span>
            ))}</p>
          </div>
        )}
      </div>

      {/* Second file upload */}
      <div>
        <h1>Second File Upload Form</h1>
        <input type="file" onChange={handleFileChange_2} />
        <button onClick={handleUpload_2}>Upload Second File</button>
        <p>{message_2}</p>
        {columns_2.length > 0 && (
          <div>
            <p>{length_2 !== null ? `Length of CSV: ${length_2}` : 'No data uploaded yet'}</p>
          </div>
        )}
        {columns_2.length > 0 && (
          <div>
            <p>Column Names: {columns_2.map((col, index) => (
              <span key={index}> {col}{index < columns_2.length - 1 ? ', ' : ''}</span>
            ))}</p>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
