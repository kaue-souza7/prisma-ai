import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { useSessionStore } from '@/store/session'

export function ProtectedRoute({ role }: { role?: 'student' | 'admin' }) {
  const { isAuthenticated, user } = useSessionStore()

  if (!isAuthenticated) return <Navigate to="/login" replace />
  if (role && user?.role !== role) return <Navigate to="/login" replace />

  return <Outlet />
}
