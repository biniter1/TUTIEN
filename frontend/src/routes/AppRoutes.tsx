import type { ReactNode } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from '../components/layout/AppLayout'
import DanhHieuPage from '../pages/DanhHieuPage'
import DongPhuPage from '../pages/DongPhuPage'
import LoginPage from '../pages/LoginPage'
import NhiemVuNgayPage from '../pages/NhiemVuNgayPage'
import RegisterPage from '../pages/RegisterPage'
import TangKinhCacPage from '../pages/TangKinhCacPage'
import ThanhTuuPage from '../pages/ThanhTuuPage'
import TuLuyenPage from '../pages/TuLuyenPage'
import { isAuthenticated } from '../store/authStore'

function ProtectedRoute({ children }: { children: ReactNode }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />
  }
  return <AppLayout>{children}</AppLayout>
}

function PublicOnlyRoute({ children }: { children: ReactNode }) {
  if (isAuthenticated()) {
    return <Navigate to="/dongphu" replace />
  }
  return <>{children}</>
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/login"
        element={
          <PublicOnlyRoute>
            <LoginPage />
          </PublicOnlyRoute>
        }
      />
      <Route
        path="/register"
        element={
          <PublicOnlyRoute>
            <RegisterPage />
          </PublicOnlyRoute>
        }
      />
      <Route
        path="/dongphu"
        element={
          <ProtectedRoute>
            <DongPhuPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/tangkinhcac"
        element={
          <ProtectedRoute>
            <TangKinhCacPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/tuluyen"
        element={
          <ProtectedRoute>
            <TuLuyenPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/nhiemvungay"
        element={
          <ProtectedRoute>
            <NhiemVuNgayPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/thanhtuu"
        element={
          <ProtectedRoute>
            <ThanhTuuPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/danhhieu"
        element={
          <ProtectedRoute>
            <DanhHieuPage />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/dongphu" replace />} />
      <Route path="*" element={<Navigate to="/dongphu" replace />} />
    </Routes>
  )
}
