import React, { useEffect, useState } from 'react';

const ergm = () => {
  const [ergmData, setErgmData] = useState(null);

  useEffect(() => {
    // Fetch the ERGM data from the Flask backend
    fetch('http://localhost:5000/get-ergm', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => {
        setErgmData(data);
      })
      .catch(error => {
        console.error('Error fetching the ERGM data:', error);
      });
      const script = document.createElement('script');
      script.src = "https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.9.3/html2pdf.bundle.min.js";
      script.async = true;
      document.body.appendChild(script);
  
      return () => {
          document.body.removeChild(script);
      };
  }, []);

  const handleDownloadERGM = () => {
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

  if (!ergmData) {
    return <p>Loading...</p>;
  }

  return (
    <>
    <div id='descriptive_stat'>
      <h2>ERGM Coefficients</h2>
      <table className='table'>
        <thead>
          <tr>
            <th>Coefficient</th>
            <th>Estimate</th>
            <th>Std. Error</th>
            <th>z value</th>
            <th>Pr(>|z|)</th>
          </tr>
        </thead>
        <tbody>
          {ergmData.coefficients.map((coef, index) => (
            <tr key={index}>
              <td>{coef.Coefficient}</td>
              <td>{coef.Estimate}</td>
              <td>{coef['Std. Error']}</td>
              <td>{coef['z value']}</td>
              <td>{coef['Pr(>|z|)']}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Significance Codes</h3>
      <p>{ergmData.significance_codes}</p>

      <h3>Deviance</h3>
      <table className='table'>
        <tbody>
          <tr>
            <th>Null Deviance</th>
            <td>{ergmData.deviance.null}</td>
          </tr>
          <tr>
            <th>Residual Deviance</th>
            <td>{ergmData.deviance.residual}</td>
          </tr>
          <tr>
            <th>DF Null</th>
            <td>{ergmData.deviance.df_null}</td>
          </tr>
          <tr>
            <th>DF Residual</th>
            <td>{ergmData.deviance.df_residual}</td>
          </tr>
        </tbody>
      </table>

      <div className='container'>
      <h3>Fit Statistics</h3>
      <table className='table'>
        <tbody>
          <tr>
            <th>AIC</th>
            <td>{ergmData.fit.AIC}</td>
          </tr>
          <tr>
            <th>BIC</th>
            <td>{ergmData.fit.BIC}</td>
          </tr>
        </tbody>
      </table>
      </div>
      <div>

    </div>
    </div>
    <div>
    <br></br>
    <br></br>
    <br></br>
    <br></br>
        <hr></hr>
        <br></br>
        <br></br>
        <br></br>
        <br></br>
        <button onClick={handleDownloadERGM}>Download report</button>
    </div>
    </>
  );
};

export default ergm;