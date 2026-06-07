import axios from 'axios'
import { clearToken, getToken } from '../store/authStore'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
})

client.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    const isAxiosError =
      typeof error === 'object' &&
      error !== null &&
      'response' in error &&
      typeof (error as { response?: { status?: number } }).response === 'object'

    if (isAxiosError) {
      const status = (error as { response: { status: number } }).response.status
      if (status === 401) {
        const currentPath = window.location.pathname
        if (currentPath !== '/login' && currentPath !== '/register') {
          clearToken()
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  },
)

export default client
