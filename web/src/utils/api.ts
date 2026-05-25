import axios from 'axios'
import { useAuth } from '../hooks/useAuth'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

api.interceptors.request.use((config) => {
  const token = useAuth.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      useAuth.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(err)
  },
)

export default api
