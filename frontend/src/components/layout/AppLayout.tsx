import type { ReactNode } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { clearToken } from '../../store/authStore'

const navItems = [
  { path: '/dongphu', label: 'Động Phủ' },
  { path: '/tangkinhcac', label: 'Tàng Kinh Các' },
  { path: '/tuluyen', label: 'Tu Luyện' },
  { path: '/nhiemvungay', label: 'Nhiệm Vụ Ngày' },
  { path: '/thanhtuu', label: 'Cơ Duyên' },
  { path: '/danhhieu', label: 'Danh Hiệu' },
]

export default function AppLayout({ children }: { children: ReactNode }) {
  const navigate = useNavigate()

  function handleLogout() {
    clearToken()
    navigate('/login')
  }

  return (
    <div className="flex min-h-screen bg-navy-950">
      <aside className="w-56 flex-shrink-0 flex flex-col bg-navy-900 border-r border-jade/10">
        <div className="px-6 py-6 border-b border-jade/10">
          <h1 className="font-display text-gold-400 text-xl font-bold leading-tight">
            Tu Tien Anh Ngu
          </h1>
          <p className="text-slate-600 text-xs mt-2 tracking-wider uppercase">
            Dao tu tien ngon ngu
          </p>
        </div>

        <nav className="flex-1 px-3 py-5 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `block px-3 py-2.5 rounded text-sm transition-colors ${
                  isActive
                    ? 'bg-jade/15 text-jade-400 border border-jade/20 font-medium'
                    : 'text-slate-500 hover:bg-navy-800 hover:text-slate-300'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="px-3 py-4 border-t border-jade/10">
          <button
            onClick={handleLogout}
            className="w-full px-3 py-2 rounded text-sm text-slate-600 hover:bg-navy-800 hover:text-slate-400 text-left transition-colors"
          >
            Thoat tu tien
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-auto min-h-screen">
        {children}
      </main>
    </div>
  )
}
