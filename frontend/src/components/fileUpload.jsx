import { useState } from 'react';
import './viewUploadResult.css'

function fileUpload({htmlTitle, flaskHost}) {
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
      const response = await fetch(flaskHost, {
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
  return (
    <>
      <div className="grid">
        <div className="container">
          <h1>{htmlTitle}</h1>
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleUpload}>Upload</button>
          <h4>{message}</h4>
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
      </div>
    </>
  );
}

export default fileUpload;