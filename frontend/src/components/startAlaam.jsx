import React, { useEffect, useState } from 'react';
import './viewUploadResult.css'

function startAlaam() {
    const [keyList, setKeyList] = useState([]);
    const [selectedKeys, setSelectedKeys] = useState([]);

    // Fetch data from the Flask backend
    useEffect(() => {
        fetch('http://localhost:5000/get-startAlaam')
            .then(response => response.json())
            .then(data => setKeyList(data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    // Handle checkbox change
    const handleCheckboxChange = (event) => {
        const { name, checked } = event.target;
        if (checked) {
            setSelectedKeys([...selectedKeys, name]);
        } else {
            setSelectedKeys(selectedKeys.filter((key) => key !== name));
        }
    };

    // Handle form submission
    const handleSubmit = (event) => {
        event.preventDefault();
        fetch('http://localhost:5000/analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ selectedKeys }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response from Flask:', data);
            // Handle the response from the backend if needed
        })
        .catch(error => console.error('Error sending data to backend:', error));
    };

    return (
        <div className='container'>
        <form onSubmit={handleSubmit}>
            {keyList.map((key, index) => (
                <div key={index}>
                    <input
                        type="checkbox"
                        id={`checkbox-${index}`}
                        name={key}
                        onChange={handleCheckboxChange}
                    />
                    <label htmlFor={`checkbox-${index}`}>{key}</label>
                </div>
            ))}
            <button type="submit">Submit</button>
        </form>
        </div>
    );
}

export default startAlaam;