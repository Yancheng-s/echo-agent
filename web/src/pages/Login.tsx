import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import api from '../utils/api'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const setToken = useAuth((s) => s.setToken)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const res = await api.post('/auth/login', { username, password })
      setToken(res.data.token)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || '登录失败')
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Echo Agent</h1>
        <p>登录你的账号</p>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="用户名"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="密码"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <div className="error">{error}</div>}
          <button type="submit">登录</button>
        </form>

        <div className="auth-footer">
          没有账号？ <Link to="/register">注册</Link>
        </div>
      </div>
    </div>
  )
}
