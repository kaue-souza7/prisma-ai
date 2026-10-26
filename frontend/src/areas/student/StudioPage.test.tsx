import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { StudioPage } from './StudioPage'
import { useSessionStore } from '@/store/session'

const apiMocks = vi.hoisted(() => ({
  getOverview: vi.fn(),
  getSummary: vi.fn(),
  getLibrary: vi.fn(),
  generate: vi.fn(),
  getGeneration: vi.fn(),
  submitExercise: vi.fn(),
}))

vi.mock('@/api', () => ({
  journeyApi: { getOverview: apiMocks.getOverview },
  progressApi: { getSummary: apiMocks.getSummary },
  studioApi: {
    generate: apiMocks.generate,
    getGeneration: apiMocks.getGeneration,
    getLibrary: apiMocks.getLibrary,
    submitExercise: apiMocks.submitExercise,
  },
}))

const phase = {
  phase: {
    id: 1,
    number: 1,
    name: 'Primeiro salário',
    description: 'Organize sua primeira renda.',
    order: 1,
  },
  status: 'in_progress',
  is_unlocked: true,
  missions: [
    {
      mission: {
        id: 10,
        phase_id: 1,
        number: 1,
        name: 'De onde vem o dinheiro?',
        description: null,
        order: 1,
        is_required: true,
        passing_score: 70,
      },
      progress: {
        mission_id: 10,
        status: 'completed',
        score: 100,
        score_percent: 100,
        attempts: 1,
        started_at: null,
        completed_at: null,
      },
      status: 'completed',
      is_unlocked: true,
    },
  ],
}

const overview = { trail: null, phases: [phase], recommendation: { kind: 'continue' } }

const revision = {
  id: 1,
  format: 'revisao',
  phase_id: 1,
  phase_name: 'Primeiro salário',
  mission_id: 10,
  mission_name: 'De onde vem o dinheiro?',
  style_hint: 'analogia com doces',
  content: {
    type: 'revisao',
    title: 'Revisão do módulo',
    sections: [{ title: 'O bruto e o líquido', body: 'O bruto é o combinado.' }],
    summary: ['Bruto não é líquido.'],
  },
  status: 'ready',
  coins_spent: 30,
  created_at: '2026-10-23T00:00:00Z',
}

const exerciseGeneration = {
  id: 2,
  format: 'exercicios',
  phase_id: 1,
  phase_name: 'Primeiro salário',
  mission_id: 10,
  mission_name: 'De onde vem o dinheiro?',
  style_hint: null,
  content: {
    type: 'exercicios',
    questions: [
      {
        prompt: 'O que é salário bruto?',
        options: [
          { value: 'a', label: 'O valor depois dos descontos.' },
          { value: 'b', label: 'O valor antes dos descontos.' },
        ],
        user_response: null,
      },
    ],
  },
  status: 'ready',
  coins_spent: 25,
  created_at: '2026-10-23T00:00:00Z',
}

const answeredExercise = {
  ...exerciseGeneration,
  content: {
    type: 'exercicios',
    questions: [
      {
        ...exerciseGeneration.content.questions[0],
        user_response: { selected_option: 'b' },
        is_correct: true,
        feedback: 'Muito bem!',
      },
    ],
    coins_rewarded: true,
  },
}

function renderStudio() {
  return render(
    <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <StudioPage />
    </MemoryRouter>,
  )
}

describe('StudioPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useSessionStore.setState({ coins: 50 })
    apiMocks.getOverview.mockResolvedValue({ data: overview })
    apiMocks.getSummary.mockResolvedValue({ data: { coins: 50 } })
    apiMocks.getLibrary.mockResolvedValue({ data: { items: [], total: 0 } })
    apiMocks.getGeneration.mockResolvedValue({ data: revision })
  })

  it('shows the balance, formats and the honest fallback when the Studio is not active', async () => {
    apiMocks.generate.mockRejectedValue({
      response: {
        status: 503,
        data: {
          error: {
            message:
              'O Estúdio estará disponível assim que o Mentor for ativado. Continue acumulando suas Prismas.',
          },
        },
      },
    })

    renderStudio()

    expect(await screen.findByText(/Transforme/)).toBeInTheDocument()
    expect(screen.getByLabelText('50 Prismas')).toBeInTheDocument()
    expect(screen.getByText('Flashcards')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /Gerar por ◆ 20/ }))

    expect(
      await screen.findByText(/O Estúdio estará disponível assim que o Mentor for ativado/),
    ).toBeInTheDocument()
    expect(apiMocks.generate).toHaveBeenCalledWith({
      format: 'flashcards',
      phase_id: 1,
      mission_id: null,
      style_hint: null,
    })
    expect(useSessionStore.getState().coins).toBe(50)
  })

  it('opens a saved review from the personal library', async () => {
    apiMocks.getLibrary.mockResolvedValue({ data: { items: [revision], total: 1 } })
    apiMocks.getGeneration.mockResolvedValue({ data: revision })

    renderStudio()

    fireEvent.click(await screen.findByRole('tab', { name: /Minha biblioteca/ }))
    fireEvent.click(await screen.findByRole('button', { name: /Revisão narrativa/ }))

    expect(apiMocks.getGeneration).toHaveBeenCalledWith(1)
    expect(await screen.findByText('O bruto e o líquido')).toBeInTheDocument()
    expect(screen.getByText('O bruto é o combinado.')).toBeInTheDocument()
  })

  it('submits an extra exercise and updates the Prism balance', async () => {
    apiMocks.generate.mockResolvedValue({ data: exerciseGeneration })
    apiMocks.getSummary
      .mockResolvedValueOnce({ data: { coins: 50 } })
      .mockResolvedValue({ data: { coins: 55 } })
    apiMocks.getGeneration.mockResolvedValue({ data: answeredExercise })
    apiMocks.submitExercise.mockResolvedValue({
      data: {
        is_correct: true,
        correct_answer: null,
        feedback: 'Muito bem!',
        all_done: true,
        coins_earned: 5,
      },
    })

    renderStudio()

    fireEvent.click(await screen.findByRole('button', { name: /Gerar por ◆ 20/ }))
    fireEvent.click(
      await screen.findByRole('radio', { name: 'O valor antes dos descontos.' }),
    )
    fireEvent.click(screen.getByRole('button', { name: /Confirmar resposta/ }))

    await waitFor(() =>
      expect(apiMocks.submitExercise).toHaveBeenCalledWith(2, 0, {
        selected_option: 'b',
      }),
    )
    expect(await screen.findByText(/Conjunto concluído/)).toBeInTheDocument()
    expect(useSessionStore.getState().coins).toBe(55)
  })
})
