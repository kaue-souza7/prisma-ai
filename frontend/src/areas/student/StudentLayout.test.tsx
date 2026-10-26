import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { StudentLayout } from './StudentLayout'
import { useSessionStore } from '@/store/session'

const apiMocks = vi.hoisted(() => ({
  getSummary: vi.fn(),
}))

vi.mock('@/api', () => ({
  progressApi: { getSummary: apiMocks.getSummary },
}))

const user = {
  id: 1,
  email: 'estudante@example.com',
  role: 'student' as const,
  is_verified: true,
}

function renderLayout() {
  return render(
    <MemoryRouter initialEntries={['/student']} future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route element={<StudentLayout />}>
          <Route path="/student" element={<div>Conteúdo inicial</div>} />
          <Route path="/student/journey" element={<div>Jornada do estudante</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  )
}

describe('StudentLayout', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    apiMocks.getSummary.mockResolvedValue({ data: { coins: 12 } })
    useSessionStore.setState({
      user,
      profile: null,
      accessToken: 'token',
      refreshToken: 'refresh',
      isAuthenticated: true,
      coins: 12,
    })
  })

  it('opens the desktop navigation drawer from the hamburger button', async () => {
    renderLayout()

    const trigger = screen.getByRole('button', { name: 'Abrir menu de navegação' })
    expect(trigger).toHaveAttribute('aria-expanded', 'false')
    expect(await screen.findByLabelText('12 Prismas')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Estúdio de Prismas' })).toBeInTheDocument()

    fireEvent.click(trigger)

    expect(trigger).toHaveAttribute('aria-expanded', 'true')
    await waitFor(() => {
      expect(screen.getByRole('button', { name: 'Fechar menu de navegação' })).toHaveFocus()
    })
  })

  it('closes the drawer with Escape and after navigating', async () => {
    renderLayout()

    const trigger = screen.getByRole('button', { name: 'Abrir menu de navegação' })
    fireEvent.click(trigger)
    fireEvent.keyDown(window, { key: 'Escape' })
    await waitFor(() => {
      expect(trigger).toHaveAttribute('aria-expanded', 'false')
    })

    fireEvent.click(trigger)
    fireEvent.click(screen.getByRole('link', { name: 'Minha jornada' }))

    expect(await screen.findByText('Jornada do estudante')).toBeInTheDocument()
    expect(trigger).toHaveAttribute('aria-expanded', 'false')
  })
})
