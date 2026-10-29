import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { OnboardingPage } from './OnboardingPage'
import { useSessionStore } from '@/store/session'

const apiMocks = vi.hoisted(() => ({
  completeOnboarding: vi.fn(),
  getAdaptiveQuestions: vi.fn(),
}))

vi.mock('@/api', () => ({
  usersApi: {
    completeOnboarding: apiMocks.completeOnboarding,
    getAdaptiveQuestions: apiMocks.getAdaptiveQuestions,
  },
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
  source: 'ai',
  version: 2,
  goal_category: 'primeiro_salario',
  phase_order: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
  trail_modes: { 1: 'express', 2: 'standard' },
  trail_1_auto_concluded: true,
  rationale: 'Começar pelo primeiro salário organiza a base.',
  focus_areas: ['Salário bruto e líquido', 'Orçamento'],
  pace: 'steady',
  next_message: 'Sua trilha está pronta. Vamos começar!',
  phases: [
    { number: 1, name: 'Meu primeiro salário', description: 'Organize sua primeira renda.' },
    { number: 2, name: 'Orçamento na prática', description: null },
  ],
}

function answerText(value: string) {
  fireEvent.change(screen.getByLabelText('Sua resposta ao Catalisador'), {
    target: { value },
  })
  fireEvent.click(screen.getByRole('button', { name: 'Enviar' }))
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
    apiMocks.getAdaptiveQuestions.mockResolvedValue({
      data: { questions: ['O que você já tentou para sair das dívidas?'], source: 'ai' },
    })
    apiMocks.completeOnboarding.mockResolvedValue({
      data: { message: 'ok', trail },
    })
  })

  it('conduz as 10 perguntas fixas, adaptativas e o consentimento até a trilha', async () => {
    renderOnboarding()

    fireEvent.click(screen.getByRole('button', { name: 'Começar' }))

    // 1 — objetivo
    fireEvent.click(
      screen.getByRole('button', { name: 'Organizar meu primeiro salário' }),
    )
    // 2 — detalhe do objetivo
    answerText('Quero organizar meu primeiro salário e guardar dinheiro.')
    // 3 — contexto de vida
    fireEvent.click(screen.getByRole('button', { name: 'Já trabalho há um tempo' }))
    // 4 — experiência formal
    answerText('3 anos')
    // 5 — padrão de renda
    fireEvent.click(screen.getByRole('button', { name: 'Tenho uma renda fixa' }))
    // 6 — maior dificuldade
    fireEvent.click(screen.getByRole('button', { name: 'Sair das dívidas' }))
    // 7 — urgência
    fireEvent.click(
      screen.getByRole('button', { name: 'Preciso resolver algo agora' }),
    )
    // 8 — nível de conhecimento
    fireEvent.click(screen.getByRole('button', { name: /Já tenho alguma base/ }))
    // 9 — estilo de aprendizagem
    fireEvent.click(
      screen.getByRole('button', { name: 'Exemplos práticos do dia a dia' }),
    )
    // 10 — sonho de 12 meses
    answerText('Guardar R$ 5.000.')

    expect(await screen.findByText('O que você já tentou para sair das dívidas?')).toBeInTheDocument()
    answerText('Já tentei planilhas, mas não mantive o hábito.')

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
          fixed_answers: expect.objectContaining({
            goal_category: 'primeiro_salario',
            life_context: 'ja_trabalho',
            urgency: 'agora_preciso',
            knowledge_level_declared: 'intermediate',
            learning_style: 'exemplos',
          }),
          conversation_history: expect.arrayContaining([
            expect.objectContaining({
              role: 'user',
              content: 'Exemplos práticos do dia a dia',
            }),
            expect.objectContaining({
              role: 'assistant',
              content: 'O que você já tentou para sair das dívidas?',
            }),
          ]),
        }),
      )
    })

    expect(
      await screen.findByRole('heading', { name: 'Sua trilha inicial está pronta.' }),
    ).toBeInTheDocument()
    expect(screen.getByText(/Começar pelo primeiro salário organiza a base/)).toBeInTheDocument()
    expect(screen.getByText(/Trilha 1 dominada no onboarding/)).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Começar jornada' }))
    expect(await screen.findByText('Área do estudante')).toBeInTheDocument()
    expect(useSessionStore.getState().profile?.onboarding_completed).toBe(true)
    expect(useSessionStore.getState().profile?.trail?.phase_order).toEqual([
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
    ])
  })
})
