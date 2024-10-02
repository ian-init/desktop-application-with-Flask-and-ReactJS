import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import Upload from './components/upload.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>

    <App />
  </StrictMode>,
)
