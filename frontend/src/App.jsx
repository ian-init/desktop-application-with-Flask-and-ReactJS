import './App.css';
import FileUpload from './components/fileUpload.jsx'

function App() {
  return (
	<>
    <FileUpload
        htmlTitle={"Attribute list"}
        flaskHost={"http://localhost:5000/upload"}
    />
    <FileUpload
      htmlTitle={"Nodes list"}
      flaskHost={"http://localhost:5000/upload_2"}
    />
	</>
  )
}
export default App;