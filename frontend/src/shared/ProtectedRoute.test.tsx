import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it } from 'vitest'

import { ProtectedRoute } from './ProtectedRoute'
import { useSessionStore } from '@/store/session'

const user = {
  id: 1,
  email: 'ana@prisma.ai',
  role: 'student',
  is_verified: true,
}

function renderProtected() {
  return render(
    <MemoryRouter
      initialEntries={['/student']}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <Routes>
        <Route path="/login" element={<div>Tela de login</div>} />
        <Route element={<ProtectedRoute role="student" />}>
          <Route path="/student" element={<div>Área protegida</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  )
}

describe('ProtectedRoute', () => {
  beforeEach(() => {
    useSessionStore.setState({
      user: null,
      profile: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
    })
    localStorage.clear()
  })

  it('redirects unauthenticated visitors to login', () => {
    renderProtected()
    expect(screen.getByText('Tela de login')).toBeInTheDocument()
  })

  it('renders the protected area for the expected role', () => {
    useSessionStore.setState({
      user,
      accessToken: 'token',
      refreshToken: 'refresh',
      isAuthenticated: true,
    })

    renderProtected()
    expect(screen.getByText('Área protegida')).toBeInTheDocument()
  })

  it('redirects users with a different role', () => {
    useSessionStore.setState({
      user: { ...user, role: 'admin' },
      accessToken: 'token',
      refreshToken: 'refresh',
      isAuthenticated: true,
    })

    renderProtected()
    expect(screen.getByText('Tela de login')).toBeInTheDocument()
  })
})
