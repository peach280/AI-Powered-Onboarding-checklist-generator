import { useState } from 'react'
import './App.css'

  function App() {
  const [url,setUrl] = useState('')
  const [checklist,setChecklist] = useState([])
  const [isLoading,setIsLoading] = useState(false)
  const [error,setError] = useState('')
  function handleChange(event)
  {
    setUrl(event.target.value)
  }
  const handleSubmit = async () => {
    if(!url) 
    {
      setError("Please enter a URL")
      return
    }
    setIsLoading(true)
    setChecklist([])
    setError('')
    try 
    {
      const backendUrl = `https://vb2128-berry-backend.hf.space/scrape?url=${encodeURIComponent(url)}`
      const response = await fetch(backendUrl)
      if(!response.ok)
      {
        throw new Error(`HTTP Error! status ${response.status}`)
      }
      const data = await response.json()
      setChecklist(data.onboarding_checklist)
    }
    catch(e)
    {
      console.error("Error fetching checklist:", e);
      setError('Failed to generate checklist. Please check the URL and try again.');
    }
    finally
    {
      setIsLoading(false)
    }
  }

  return (
    <div className='container'>
      <h1>Generate AI Powered Onboarding Checklist</h1>
      <div className='form'>
      <input
      type='text'
      placeholder='Enter documentation URL'
      value={url}
      onChange={handleChange}
      />
      <button onClick={handleSubmit} disabled={isLoading}>
        {isLoading? 'Generating....':'Generate'}
      </button>
      </div>
      {error && <p className="error">{error}</p>}
      <div className='checklist'>
        {checklist.map((item,index)=>(
          <div key={index} className='checklistItem'>
            <input type="checkbox" id={`item-${index}`}/>
            <label htmlFor={`item-${index}`}>{item}</label>
          </div>
        ))}
      </div>
    </div>
    
  )
}

export default App
