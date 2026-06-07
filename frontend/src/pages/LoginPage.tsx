import { type FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login } from '../api/auth'
import { setToken } from '../store/authStore'

export default function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await login({ email, password })
      setToken(data.access_token)
      navigate('/dongphu')
    } catch {
      setError('Sai email hoac mat khau. Xin thu lai.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-navy-950 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-10">
          <h1 className="font-display text-4xl text-gold-400 font-bold">Tu Tien Anh Ngu</h1>
          <p className="text-slate-500 mt-3 text-sm">
            Buoc vao con duong tu tien ngon ngu
          </p>
        </div>

        <div className="bg-navy-800 border border-gold/20 rounded-xl p-8 shadow-2xl">
          <h2 className="text-jade-400 text-base font-semibold mb-6 tracking-wide uppercase">
            Dang Nhap
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-slate-400 text-xs mb-1.5 uppercase tracking-wider">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                className="w-full bg-navy-900 border border-navy-600 text-slate-200 rounded px-3 py-2.5 text-sm focus:outline-none focus:border-jade/40 transition-colors"
                placeholder="dao@tu-tien.vn"
              />
            </div>

            <div>
              <label className="block text-slate-400 text-xs mb-1.5 uppercase tracking-wider">
                Mat khau
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                className="w-full bg-navy-900 border border-navy-600 text-slate-200 rounded px-3 py-2.5 text-sm focus:outline-none focus:border-jade/40 transition-colors"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <p className="text-red-400 text-sm py-1">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-jade hover:bg-jade-500 text-navy-950 font-semibold rounded px-4 py-2.5 text-sm transition-colors disabled:opacity-50 mt-2"
            >
              {loading ? 'Dang xu ly...' : 'Buoc vao tu tien'}
            </button>
          </form>

          <p className="text-slate-600 text-sm mt-6 text-center">
            Chua co tai khoan?{' '}
            <Link to="/register" className="text-jade-400 hover:text-jade-300 transition-colors">
              Dang ky
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
