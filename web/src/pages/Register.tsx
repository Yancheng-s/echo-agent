import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../utils/api'

export default function Register() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (password !== confirm) {
      setError('两次密码不一致')
      return
    }
    try {
      await api.post('/auth/register', { username, password })
      navigate('/login')
    } catch (err: any) {
      setError(err.response?.data?.detail || '注册失败')
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Echo Agent</h1>
        <p>创建新账号</p>

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
          <input
            type="password"
            placeholder="确认密码"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
          {error && <div className="error">{error}</div>}
          <button type="submit">注册</button>
        </form>

        <div className="auth-footer">
          已有账号？ <Link to="/login">登录</Link>
        </div>
      </div>
    </div>
  )
}
