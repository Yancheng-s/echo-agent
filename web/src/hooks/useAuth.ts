import { create } from 'zustand'

interface AuthState {
  token: string | null
  setToken: (token: string | null) => void
  isAuthenticated: () => boolean
  logout: () => void
}

export const useAuth = create<AuthState>((set, get) => ({
  token: localStorage.getItem('token'),

  setToken: (token) => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
    set({ token })
  },

  isAuthenticated: () => !!get().token,

  logout: () => {
    localStorage.removeItem('token')
    set({ token: null })
  },
}))
