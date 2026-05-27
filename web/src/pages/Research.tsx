import { useState } from 'react'

export default function Research() {
  const [query, setQuery] = useState('')

  return (
    <div className="app">
      <header className="header">
        <h1>Echo Agent</h1>
        <p>Deep Research — 回声探测，深层发现</p>
      </header>

      <main className="main">
        <div className="input-area">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="输入你的研究问题..."
            rows={3}
          />
          <button disabled={!query.trim()}>开始研究</button>
        </div>
      </main>
    </div>
  )
}
