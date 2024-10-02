import { useState } from 'react';
import './App.css';
import fileUpload from './components/fileUpload.jsx'

function App() {
  <>
    <Mod htmlTitle={"Attribute list"}
        flaskHost={"http://localhost:5000/upload"}
    />
    <Mod
      htmlTitle={"Nodes list"}
      flaskHost={"http://localhost:5000/upload_2"}
    />
  </>
export default App;
