import { useState } from 'react';

function fileUpload({htmlTitle, flaskHost}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [length, setLength] = useState(null);  // State to hold the length of the dataframe
  const [columns, setColumns] = useState([]);  // State to hold the column names

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    console.log(flaskHost);
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
      <div>
        <h1>{htmlTitle}</h1>
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
    </>
  );
}

export default fileUpload;