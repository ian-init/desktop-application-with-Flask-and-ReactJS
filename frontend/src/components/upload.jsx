import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid2';
import './upload.css'



function upload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        alert('File uploaded successfully!');
      } else {
        alert('File upload failed.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <>
    <div className='container'>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={{xs: 3, md: 2}} style={{paddingTop: '3vh'}}>
          <Grid size={{ xs: 18, md: 9 }}>       
            <div className='cell' style={{backgroundColor: 'White', color: 'black', borderColor: 'red'}}>
              <h2>File Upload Form</h2>
              <form action="/upload" method="post" enctype="multipart/form-data">
                <label for="file">Select a file to upload:</label>
                <input type="file" id="file" name="file"></input>
                <input type="submit" value="Upload"></input>
              </form>
            </div>
          </Grid>
        </Grid>

      </Box>
    </div>
    </>
  );
}



export default upload;