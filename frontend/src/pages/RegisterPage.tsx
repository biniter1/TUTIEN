import { type FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register } from '../api/auth'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [daoName, setDaoName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register({
        email,
        username,
        password,
        dao_name: daoName.trim() || undefined,
      })
      navigate('/login')
    } catch {
      setError('Dang ky that bai. Email hoac ten co the da duoc su dung.')
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
            Dang ky de bat dau hanh trinh tu tien
          </p>
        </div>

        <div className="bg-navy-800 border border-gold/20 rounded-xl p-8 shadow-2xl">
          <h2 className="text-jade-400 text-base font-semibold mb-6 tracking-wide uppercase">
            Dang Ky
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
                Ten nguoi dung
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoComplete="username"
                className="w-full bg-navy-900 border border-navy-600 text-slate-200 rounded px-3 py-2.5 text-sm focus:outline-none focus:border-jade/40 transition-colors"
                placeholder="tuthien_123"
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
                autoComplete="new-password"
                className="w-full bg-navy-900 border border-navy-600 text-slate-200 rounded px-3 py-2.5 text-sm focus:outline-none focus:border-jade/40 transition-colors"
                placeholder="••••••••"
              />
            </div>

            <div>
              <label className="block text-slate-400 text-xs mb-1.5 uppercase tracking-wider">
                Dao hieu <span className="text-slate-600 normal-case">(tuy chon)</span>
              </label>
              <input
                type="text"
                value={daoName}
                onChange={(e) => setDaoName(e.target.value)}
                className="w-full bg-navy-900 border border-navy-600 text-slate-200 rounded px-3 py-2.5 text-sm focus:outline-none focus:border-jade/40 transition-colors"
                placeholder="Thanh Van Tu Si..."
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
              {loading ? 'Dang tao tai khoan...' : 'Bat dau tu tien'}
            </button>
          </form>

          <p className="text-slate-600 text-sm mt-6 text-center">
            Da co tai khoan?{' '}
            <Link to="/login" className="text-jade-400 hover:text-jade-300 transition-colors">
              Dang nhap
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
