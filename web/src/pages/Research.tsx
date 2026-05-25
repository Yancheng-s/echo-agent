import { useState } from 'react'
import { useAuth } from '../hooks/useAuth'

export default function Research() {
  const [query, setQuery] = useState('')
  const logout = useAuth((s) => s.logout)

  return (
    <div className="app">
      <header className="header">
        <div className="header-top">
          <h1>Echo Agent</h1>
          <button className="logout-btn" onClick={logout}>退出</button>
        </div>
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
