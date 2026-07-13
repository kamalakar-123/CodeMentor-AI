function Home({ welcomeMessage, loading, error, apiBaseUrl }) {
  return (
    <main className="page-shell">
      <section className="hero-card">
        <p className="eyebrow">CodeMentor AI</p>
        <h1>AI-Powered Coding Interview Preparation Platform</h1>
        <p className="subtitle">
          A clean Day 1 starter that connects a React frontend to a FastAPI backend.
        </p>

        <div className="status-card">
          <h2>Backend Status</h2>

          {loading ? <p className="loading-text">Loading backend welcome message...</p> : null}

          {error ? <p className="error-text">Error: {error}</p> : null}

          {!loading && !error ? <p className="success-text">{welcomeMessage}</p> : null}

          <p className="api-note">API base URL: {apiBaseUrl}</p>
        </div>
      </section>
    </main>
  )
}

export default Home
