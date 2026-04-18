import { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const trimmedQuestion = question.trim();
    if (!trimmedQuestion) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: trimmedQuestion })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get response');
      }

      setAnswer(data.answer);
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Cognitia AI</h1>
      <p className="subtitle">Ask a question, get an instant answer</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <div className="input-wrapper">
            <input
              type="text"
              className="input-field"
              placeholder="Ask me anything..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={loading}
              maxLength={1000}
            />
            <button
              type="submit"
              className="submit-btn"
              disabled={loading || !question.trim()}
            >
              {loading ? 'Asking...' : 'Ask'}
            </button>
          </div>
        </div>
      </form>

      {error && (
        <div className="response-container">
          <div className="error-box">{error}</div>
        </div>
      )}

      {loading && (
        <div className="response-container">
          <div className="response-label">Response</div>
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      {!loading && answer && (
        <div className="response-container">
          <div className="response-label">Response</div>
          <div className="response-box">{answer}</div>
        </div>
      )}
    </div>
  );
}

export default App;