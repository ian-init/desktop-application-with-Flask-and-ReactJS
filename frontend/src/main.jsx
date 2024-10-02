import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'

import fileUpload from './components/fileUpload.jsx'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <fileUpload
        htmlTitle={"Attribute list"}
        flaskHost={"http://localhost:5000/upload"}
    />
  </StrictMode>,
)
