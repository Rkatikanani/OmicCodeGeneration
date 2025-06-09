import { useState, FormEvent } from 'react'
import './App.css'

interface ApiResponse {
  generated_code: string;
  explanation: string;
  metadata: {
    model: string;
  };
}

function App() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ApiResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:8000/generate-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          natural_language: input,
          analysis_type: 'RNA-seq' // You can make this dynamic later
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to generate code')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Omic Code Generator</h1>
      
      <form onSubmit={handleSubmit} className="form">
        <div className="input-group">
          <label htmlFor="input">Describe your analysis:</label>
          <textarea
            id="input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g., Perform differential gene expression analysis on RNA-seq data"
            rows={4}
          />
        </div>
        
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? 'Generating...' : 'Generate Code'}
        </button>
      </form>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {result && (
        <div className="result">
          <h2>Generated Code:</h2>
          <pre className="code-block">
            {result.generated_code}
          </pre>
          
          <h2>Explanation:</h2>
          <p className="explanation">
            {result.explanation}
          </p>
        </div>
      )}
    </div>
  )
}

export default App
