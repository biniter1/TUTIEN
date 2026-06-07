import axios from 'axios'
import type { User } from '../types/api'

const authClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
})

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  dao_name?: string
}

export async function login(data: LoginRequest): Promise<LoginResponse> {
  const res = await authClient.post<LoginResponse>('/auth/login', data)
  return res.data
}

export async function register(data: RegisterRequest): Promise<User> {
  const res = await authClient.post<User>('/auth/register', data)
  return res.data
}
