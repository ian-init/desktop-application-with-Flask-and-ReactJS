import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import AttributeDescriptiveStat from './attributeDescriptiveStat.jsx'
import NodeDescriptiveStat from './nodeDescriptiveStat.jsx'


function viewUploadResult () {
    return (
    <>
    <AttributeDescriptiveStat />
    <NodeDescriptiveStat />
      
	</>
  )
}
export default viewUploadResult;