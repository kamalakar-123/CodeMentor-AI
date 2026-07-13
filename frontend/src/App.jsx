import { useEffect, useState } from 'react'
import Home from './pages/Home'


// Use the backend URL from the environment when available.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'


function App() {
  // Store the welcome message returned by FastAPI.
  const [welcomeMessage, setWelcomeMessage] = useState('')

  // Track whether the request is still in progress.
  const [loading, setLoading] = useState(true)

  // Track any request error so the UI can explain the problem.
  const [error, setError] = useState('')

  useEffect(() => {
    // Create a small async function so we can use await inside the effect.
    const fetchWelcomeMessage = async () => {
      try {
        // Start in a loading state and clear any previous error.
        setLoading(true)
        setError('')

        // Call the FastAPI root endpoint.
        const response = await fetch(`${API_BASE_URL}/`)

        // Stop early if the server returned an error response.
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`)
        }

        // Parse the JSON body returned by FastAPI.
        const data = await response.json()

        // Store the message for the Home page to display.
        setWelcomeMessage(data.message ?? 'No welcome message was returned.')
      } catch (requestError) {
        // Convert the unknown error into a readable message.
        const message = requestError instanceof Error ? requestError.message : 'Unknown error'
        setError(message)
      } finally {
        // Stop the loading indicator once the request finishes.
        setLoading(false)
      }
    }

    // Run the fetch logic when the component mounts.
    fetchWelcomeMessage()
  }, [])

  // Render the Home page and pass the API data as props.
  return <Home welcomeMessage={welcomeMessage} loading={loading} error={error} apiBaseUrl={API_BASE_URL} />
}

export default App
