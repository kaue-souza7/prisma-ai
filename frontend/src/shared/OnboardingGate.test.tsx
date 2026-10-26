import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { OnboardingGate } from './OnboardingGate'
import { useSessionStore } from '@/store/session'

const apiMocks = vi.hoisted(() => ({
  getMe: vi.fn(),
}))

vi.mock('@/api', () => ({
  usersApi: { getMe: apiMocks.getMe },
}))

const baseProfile = {
  personal_goal: null,
  knowledge_level: null,
  onboarding_completed: false,
  consent_given: false,
  preferences: null,
}

function renderGate() {
  return render(
    <MemoryRouter
      initialEntries={['/student']}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <Routes>
        <Route path="/onboarding" element={<div>Tela de onboarding</div>} />
        <Route element={<OnboardingGate />}>
          <Route path="/student" element={<div>Jornada liberada</div>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  )
}

describe('OnboardingGate', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useSessionStore.setState({
      user: { id: 1, email: 'ana@prisma.ai', role: 'student', is_verified: true },
      profile: null,
      accessToken: 'token',
      refreshToken: 'refresh',
      isAuthenticated: true,
    })
  })

  it('redirects a student who has not completed onboarding', async () => {
    apiMocks.getMe.mockResolvedValue({
      data: {
        user: { id: 1, email: 'ana@prisma.ai', role: 'student', is_verified: true },
        profile: baseProfile,
      },
    })

    renderGate()

    expect(await screen.findByText('Tela de onboarding')).toBeInTheDocument()
  })

  it('releases the journey only after onboarding is complete', async () => {
    apiMocks.getMe.mockResolvedValue({
      data: {
        user: { id: 1, email: 'ana@prisma.ai', role: 'student', is_verified: true },
        profile: { ...baseProfile, onboarding_completed: true, consent_given: true },
      },
    })

    renderGate()

    expect(await screen.findByText('Jornada liberada')).toBeInTheDocument()
    expect(useSessionStore.getState().profile?.onboarding_completed).toBe(true)
  })
})
