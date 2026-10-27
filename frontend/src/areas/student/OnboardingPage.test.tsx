import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { OnboardingPage } from './OnboardingPage'
import { useSessionStore } from '@/store/session'

const apiMocks = vi.hoisted(() => ({
  completeOnboarding: vi.fn(),
}))

vi.mock('@/api', () => ({
  usersApi: { completeOnboarding: apiMocks.completeOnboarding },
}))

function renderOnboarding() {
  return render(
    <MemoryRouter
      initialEntries={['/onboarding']}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <Routes>
        <Route path="/onboarding" element={<OnboardingPage />} />
        <Route path="/student" element={<div>Área do estudante</div>} />
      </Routes>
    </MemoryRouter>,
  )
}

const trail = {
  source: 'rules',
  version: 1,
  goal_category: 'primeiro_salario',
  phase_order: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  rationale: 'Começar pelo primeiro salário organiza a base.',
  focus_areas: ['Salário bruto e líquido', 'Orçamento'],
  pace: 'steady',
  phases: [
    { number: 1, name: 'Meu primeiro salário', description: 'Organize sua primeira renda.' },
    { number: 2, name: 'Orçamento na prática', description: null },
  ],
}

describe('OnboardingPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useSessionStore.setState({
      user: { id: 1, email: 'ana@prisma.ai', role: 'student', is_verified: true },
      profile: null,
      accessToken: 'token',
      refreshToken: 'refresh',
      isAuthenticated: true,
    })
    apiMocks.completeOnboarding.mockResolvedValue({
      data: { message: 'ok', trail },
    })
  })

  it('collects goal, knowledge level and LGPD consent before showing the trail', async () => {
    renderOnboarding()

    fireEvent.click(screen.getByRole('button', { name: 'Começar' }))
    fireEvent.click(
      screen.getByRole('radio', { name: 'Organizar meu primeiro salário' }),
    )
    fireEvent.click(
      screen.getByRole('radio', { name: /Já tenho alguma base/ }),
    )
    fireEvent.click(screen.getByRole('button', { name: 'Continuar' }))

    const finish = screen.getByRole('button', { name: 'Montar minha trilha' })
    expect(finish).toBeDisabled()

    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(finish)

    await waitFor(() => {
      expect(apiMocks.completeOnboarding).toHaveBeenCalledWith(
        expect.objectContaining({
          personal_goal: 'Organizar meu primeiro salário',
          knowledge_level: 'intermediate',
          consent_version: '2026-10-21',
        }),
      )
    })
    expect(
      await screen.findByRole('heading', { name: 'Sua trilha inicial está pronta.' }),
    ).toBeInTheDocument()
    expect(screen.getByText(/Começar pelo primeiro salário organiza a base/)).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Começar jornada' }))
    expect(await screen.findByText('Área do estudante')).toBeInTheDocument()
    expect(useSessionStore.getState().profile?.onboarding_completed).toBe(true)
    expect(useSessionStore.getState().profile?.trail?.phase_order).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
  })
})
