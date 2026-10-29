import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { LessonPlayerPage } from './LessonPlayerPage'
import { useSessionStore } from '@/store/session'
import styles from './LessonPlayer.module.css'

const apiMocks = vi.hoisted(() => ({
  getLesson: vi.fn(),
  startMission: vi.fn(),
  saveLessonStep: vi.fn(),
  submitResponse: vi.fn(),
  retryMission: vi.fn(),
}))

vi.mock('@/api', () => ({
  journeyApi: {
    getLesson: apiMocks.getLesson,
    startMission: apiMocks.startMission,
    saveLessonStep: apiMocks.saveLessonStep,
    submitResponse: apiMocks.submitResponse,
    retryMission: apiMocks.retryMission,
  },
}))

const activity = {
  id: 101,
  order: 1,
  activity_type: 'multiple_choice',
  points_value: 10,
  content: {
    prompt: 'O que significa salário bruto?',
    options: [
      { value: 'a', label: 'O valor depois dos descontos.' },
      { value: 'b', label: 'O valor antes dos descontos.' },
    ],
  },
}

const baseLesson = {
  mission: {
    id: 10,
    phase_id: 1,
    number: 1,
    name: 'De onde vem o dinheiro?',
    description: 'Diferencie bruto de líquido.',
    order: 1,
    is_required: true,
    passing_score: 70,
  },
  phase: { id: 1, number: 1, name: 'Primeiro salário', description: null, order: 1 },
  competencies: [
    { id: 1, code: '1.1.1', name: 'Distinguir salário bruto de líquido', is_essential: true },
  ],
  steps: [
    {
      index: 0,
      type: 'intro',
      title: 'O dinheiro que chega não é o dinheiro que fica',
      body: 'Uma introdução ao contracheque.',
      agent: 'catalyst',
      content_type: null,
      highlights: ['Diferenciar bruto de líquido'],
      activity: null,
      user_response: null,
      completed: false,
    },
    {
      index: 1,
      type: 'reading',
      title: 'O que é salário bruto e líquido',
      body: 'O **bruto** é o valor combinado antes dos descontos.',
      agent: 'mentor',
      content_type: 'explanation',
      highlights: [],
      activity: null,
      user_response: null,
      completed: false,
    },
    {
      index: 2,
      type: 'question',
      title: 'O que significa salário bruto?',
      body: null,
      agent: 'mentor',
      content_type: null,
      highlights: [],
      activity,
      user_response: null,
      completed: false,
    },
    {
      index: 3,
      type: 'summary',
      title: 'Seu contracheque agora faz sentido',
      body: 'Você aprendeu a olhar o salário em camadas.',
      agent: 'analyst',
      content_type: null,
      highlights: ['Bruto é o valor combinado.'],
      activity: null,
      user_response: null,
      completed: false,
    },
  ],
  current_step: 0,
  completed_steps: [],
  estimated_minutes: 12,
  status: 'available',
  progress: null,
  next_mission: null,
}

function renderLesson() {
  return render(
    <MemoryRouter
      initialEntries={['/student/learn/10']}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <Routes>
        <Route path="/student/learn/:missionId" element={<LessonPlayerPage />} />
        <Route path="/student/journey" element={<div>Minha jornada</div>} />
      </Routes>
    </MemoryRouter>,
  )
}

describe('LessonPlayerPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    useSessionStore.setState({ coins: 0 })
    apiMocks.getLesson.mockResolvedValue({ data: baseLesson })
    apiMocks.startMission.mockResolvedValue({ data: { status: 'in_progress' } })
    apiMocks.retryMission.mockResolvedValue({ data: { status: 'in_progress', attempts: 2 } })
    apiMocks.saveLessonStep.mockResolvedValue({
      data: { current_step: 1, completed_steps: [0], mission_completed: false },
    })
    apiMocks.submitResponse.mockResolvedValue({
      data: {
        is_correct: true,
        score: 10,
        feedback: 'Exato! O bruto é o valor antes dos descontos.',
        attempt_number: 1,
        mission_completed: false,
        points_earned: 0,
        coins_earned: 2,
        new_achievements: [],
      },
    })
  })

  it('starts the module and advances to the first reading screen', async () => {
    renderLesson()

    expect(
      await screen.findByRole('heading', {
        name: 'O dinheiro que chega não é o dinheiro que fica',
      }),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /Começar módulo/ }))

    await waitFor(() => expect(apiMocks.startMission).toHaveBeenCalledWith(10))
    expect(await screen.findByRole('heading', { name: 'O que é salário bruto e líquido' })).toBeInTheDocument()
    expect(apiMocks.saveLessonStep).toHaveBeenCalledWith(10, 0)
  })

  it('reloads the lesson after starting so the drawn question set is used', async () => {
    const refreshedLesson = {
      ...baseLesson,
      status: 'in_progress',
      steps: baseLesson.steps.map((step) =>
        step.index === 2
          ? {
              ...step,
              title: 'Pergunta do conjunto sorteado',
              activity: {
                ...activity,
                id: 202,
                content: {
                  ...activity.content,
                  prompt: 'Pergunta do conjunto sorteado',
                },
              },
            }
          : step,
      ),
    }
    apiMocks.getLesson
      .mockResolvedValueOnce({ data: baseLesson })
      .mockResolvedValueOnce({ data: refreshedLesson })
    apiMocks.saveLessonStep
      .mockResolvedValueOnce({
        data: { current_step: 1, completed_steps: [0], mission_completed: false },
      })
      .mockResolvedValueOnce({
        data: { current_step: 2, completed_steps: [0, 1], mission_completed: false },
      })

    renderLesson()

    fireEvent.click(
      await screen.findByRole('button', { name: /Começar módulo/ }),
    )

    await waitFor(() => expect(apiMocks.getLesson).toHaveBeenCalledTimes(2))
    fireEvent.click(await screen.findByRole('button', { name: /^Continuar$/ }))

    expect(
      await screen.findByRole('heading', {
        name: 'Pergunta do conjunto sorteado',
      }),
    ).toBeInTheDocument()
  })

  it('requires confirmation and shows feedback before advancing', async () => {
    apiMocks.getLesson.mockResolvedValue({
      data: {
        ...baseLesson,
        current_step: 2,
        completed_steps: [0, 1],
        status: 'in_progress',
      },
    })
    apiMocks.saveLessonStep.mockResolvedValue({
      data: { current_step: 3, completed_steps: [0, 1, 2], mission_completed: false },
    })

    renderLesson()

    expect(await screen.findByRole('heading', { name: 'O que significa salário bruto?' })).toBeInTheDocument()
    expect(screen.queryByText(/Exato! O bruto/)).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('radio', { name: 'O valor antes dos descontos.' }))
    fireEvent.click(screen.getByRole('button', { name: /Confirmar resposta/ }))

    expect(await screen.findByText('Resposta correta')).toBeInTheDocument()
    expect(screen.getByText('Exato! O bruto é o valor antes dos descontos.')).toBeInTheDocument()
    expect(apiMocks.submitResponse).toHaveBeenCalledWith(10, 101, { selected_option: 'b' })
    expect(useSessionStore.getState().coins).toBe(2)

    fireEvent.click(screen.getByRole('button', { name: /Continuar/ }))

    expect(await screen.findByRole('heading', { name: 'Seu contracheque agora faz sentido' })).toBeInTheDocument()
  })

  it('lets the student rewrite an open answer when the Mentor needs clarification', async () => {
    const openTextActivity = {
      id: 303,
      order: 1,
      activity_type: 'open_text',
      points_value: 0,
      content: {
        prompt: 'Explique a diferença entre salário bruto e líquido.',
        max_length: 2000,
      },
    }
    apiMocks.getLesson.mockResolvedValue({
      data: {
        ...baseLesson,
        current_step: 2,
        completed_steps: [0, 1],
        status: 'in_progress',
        steps: baseLesson.steps.map((step) =>
          step.index === 2
            ? {
                ...step,
                title: openTextActivity.content.prompt,
                activity: openTextActivity,
              }
            : step,
        ),
      },
    })
    apiMocks.submitResponse.mockResolvedValue({
      data: {
        is_correct: null,
        score: 0,
        feedback: 'Pode complementar sua resposta com um exemplo?',
        evaluation_status: 'ambiguous',
        attempt_number: 1,
        mission_completed: false,
        points_earned: 0,
        new_achievements: [],
      },
    })

    renderLesson()

    const textarea = await screen.findByPlaceholderText(
      'Escreva com as suas palavras...',
    )
    fireEvent.change(textarea, { target: { value: 'Acho que tem a ver com descontos.' } })
    fireEvent.click(screen.getByRole('button', { name: /Confirmar resposta/ }))

    expect(await screen.findByText('Preciso de mais contexto')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Reescrever resposta' }),
    ).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Reescrever resposta' }))

    expect(screen.getByRole('button', { name: /Confirmar resposta/ })).toBeInTheDocument()
    expect(textarea).not.toBeDisabled()
  })

  it('animates the Mentor while the open answer is being analyzed', async () => {
    const openTextActivity = {
      id: 304,
      order: 1,
      activity_type: 'open_text',
      points_value: 0,
      content: {
        prompt: 'Explique a diferença entre salário bruto e líquido.',
        max_length: 2000,
      },
    }
    apiMocks.getLesson.mockResolvedValue({
      data: {
        ...baseLesson,
        current_step: 2,
        completed_steps: [0, 1],
        status: 'in_progress',
        steps: baseLesson.steps.map((step) =>
          step.index === 2
            ? {
                ...step,
                title: openTextActivity.content.prompt,
                activity: openTextActivity,
              }
            : step,
        ),
      },
    })

    let resolveSubmit!: (value: unknown) => void
    const pendingSubmit = new Promise((resolve) => {
      resolveSubmit = resolve
    })
    apiMocks.submitResponse.mockReturnValue(pendingSubmit)

    renderLesson()

    const textarea = await screen.findByPlaceholderText(
      'Escreva com as suas palavras...',
    )
    fireEvent.change(textarea, { target: { value: 'O bruto é antes dos descontos.' } })
    fireEvent.click(screen.getByRole('button', { name: /Confirmar resposta/ }))

    expect(await screen.findByText('Analisando sua resposta...')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: /Mentor analisando/ }),
    ).toBeDisabled()

    await act(async () => {
      resolveSubmit({
        data: {
          is_correct: true,
          score: 0,
          feedback: 'Boa explicação.',
          evaluation_status: 'correct',
          attempt_number: 1,
          mission_completed: false,
          points_earned: 0,
          new_achievements: [],
        },
      })
    })

    expect(await screen.findByText('Resposta correta')).toBeInTheDocument()
    expect(screen.queryByText('Analisando sua resposta...')).not.toBeInTheDocument()
  })

  it('adds the Analyst recommendation when an error repeats', async () => {
    apiMocks.getLesson.mockResolvedValue({
      data: {
        ...baseLesson,
        current_step: 2,
        completed_steps: [0, 1],
        status: 'in_progress',
      },
    })
    apiMocks.submitResponse.mockResolvedValue({
      data: {
        is_correct: false,
        score: 0,
        feedback: 'O bruto é o valor antes dos descontos. Revise a diferença.',
        feedback_agent: 'analyst',
        attempt_number: 2,
        reinforcement: {
          agent: 'analyst',
          severity: 'attention',
          action: 'review',
          competencies: ['Distinguir salário bruto de líquido'],
          message: 'Esse conceito apareceu com dificuldade. Releia o trecho e tente de novo.',
        },
        mission_completed: false,
        points_earned: 0,
        new_achievements: [],
      },
    })

    renderLesson()

    fireEvent.click(
      await screen.findByRole('radio', { name: 'O valor depois dos descontos.' }),
    )
    fireEvent.click(screen.getByRole('button', { name: /Confirmar resposta/ }))

    expect(await screen.findByText('Feedback do Mentor')).toBeInTheDocument()
    expect(await screen.findByText('Analista de Progresso')).toBeInTheDocument()
    expect(
      screen.getByText(/Esse conceito apareceu com dificuldade/),
    ).toBeInTheDocument()
  })

  it('shows the Analyst and Catalyst summaries after completing a mission', async () => {
    apiMocks.saveLessonStep.mockResolvedValueOnce({
      data: { current_step: 3, completed_steps: [0, 1, 2, 3], mission_completed: true },
    })
    apiMocks.getLesson.mockResolvedValue({
      data: {
        ...baseLesson,
        current_step: 3,
        completed_steps: [0, 1, 2],
        status: 'completed',
        progress: {
          mission_id: 10,
          status: 'completed',
          score: 100,
          score_percent: 100,
          attempts: 1,
          started_at: null,
          completed_at: null,
        },
        mission_insight: {
          agent: 'analyst',
          severity: 'positive',
          action: 'advance',
          competencies: ['Distinguir salário bruto de líquido'],
          message: 'Você demonstrou o conceito nesta missão.',
        },
        next_step: {
          kind: 'start',
          message: 'Seu próximo passo é a missão 1.2.',
          mission_id: 11,
          mission_name: 'O que importa primeiro?',
          phase_number: 1,
          phase_name: 'Primeiro salário',
          trail_position: 1,
          trail_size: 6,
        },
      },
    })

    renderLesson()

    expect(
      await screen.findByRole('heading', { name: 'Seu contracheque agora faz sentido' }),
    ).toBeInTheDocument()
    expect(screen.getByText('Você demonstrou o conceito nesta missão.')).toBeInTheDocument()
    expect(screen.getByText('Seu próximo passo é a missão 1.2.')).toBeInTheDocument()
    expect(screen.getByText('100%')).toBeInTheDocument()
    expect(screen.getByText('Aprovado ✓')).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: /Conversar com o Mentor sobre este módulo/ }),
    ).toBeInTheDocument()
  })

  it('toggles optional sound and tactile effects', async () => {
    renderLesson()

    const toggle = await screen.findByRole('button', { name: 'Ativar efeitos sonoros' })
    fireEvent.click(toggle)

    expect(
      screen.getByRole('button', { name: 'Desativar efeitos sonoros' }),
    ).toHaveAttribute('aria-pressed', 'true')
    expect(localStorage.getItem('ell-learning-effects')).toBe('1')
  })

  it('reveals the correct answer and allows continuing after an error', async () => {
    apiMocks.getLesson.mockResolvedValue({
      data: {
        ...baseLesson,
        current_step: 2,
        completed_steps: [0, 1],
        status: 'in_progress',
      },
    })
    apiMocks.submitResponse.mockResolvedValue({
      data: {
        is_correct: false,
        correct_answer: 'b',
        score: 0,
        feedback: 'O bruto é o valor antes dos descontos. Revise a diferença.',
        attempt_number: 1,
        mission_completed: false,
        attempt_finished: true,
        points_earned: 0,
        new_achievements: [],
        score_percent: 0,
        passed: false,
        must_retry: true,
        can_retry_optionally: false,
      },
    })

    renderLesson()

    fireEvent.click(
      await screen.findByRole('radio', { name: 'O valor depois dos descontos.' }),
    )
    fireEvent.click(screen.getByRole('button', { name: /Confirmar resposta/ }))

    expect(await screen.findByText('Feedback do Mentor')).toBeInTheDocument()
    expect(
      screen.queryByRole('button', { name: /Tentar novamente/ }),
    ).not.toBeInTheDocument()
    expect(
      screen.getByText('A resposta correta está destacada em verde.'),
    ).toBeInTheDocument()

    const wrongOption = screen
      .getByRole('radio', { name: 'O valor depois dos descontos.' })
      .closest('label')
    const correctOption = screen
      .getByRole('radio', { name: 'O valor antes dos descontos.' })
      .closest('label')
    expect(wrongOption).toHaveClass(styles.optionWrong)
    expect(correctOption).toHaveClass(styles.optionCorrect)

    fireEvent.click(screen.getByRole('button', { name: /Continuar/ }))
    await waitFor(() => expect(apiMocks.saveLessonStep).toHaveBeenCalledWith(10, 2))
  })

  it('shows the percentage and offers a mandatory retry after failing', async () => {
    apiMocks.saveLessonStep.mockResolvedValueOnce({
      data: { current_step: 3, completed_steps: [0, 1, 2], mission_completed: false },
    })
    apiMocks.getLesson
      .mockResolvedValueOnce({
        data: {
          ...baseLesson,
          current_step: 3,
          completed_steps: [0, 1, 2],
          status: 'in_progress',
          score_percent: 60,
          passed: false,
          attempt_finished: true,
          must_retry: true,
          can_retry_optionally: false,
          progress: {
            mission_id: 10,
            status: 'in_progress',
            score: null,
            score_percent: 60,
            attempts: 1,
            started_at: null,
            completed_at: null,
          },
          steps: baseLesson.steps.map((step) =>
            step.index === 2
              ? {
                  ...step,
                  completed: true,
                  user_response: {
                    is_correct: false,
                    feedback: 'Revise o conceito.',
                    attempt_number: 1,
                    response_data: {},
                    correct_answer: 'b',
                  },
                }
              : step,
          ),
        },
      })
      .mockResolvedValueOnce({
        data: { ...baseLesson, current_step: 0, status: 'in_progress' },
      })

    renderLesson()

    expect(await screen.findByText('60%')).toBeInTheDocument()
    expect(screen.getByText('Refaça para avançar ✗')).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: /Próximo módulo/ })).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /^Refazer módulo$/ }))

    await waitFor(() => expect(apiMocks.retryMission).toHaveBeenCalledWith(10, false))
    expect(
      await screen.findByRole('heading', {
        name: 'O dinheiro que chega não é o dinheiro que fica',
      }),
    ).toBeInTheDocument()
  })

  it('offers the next module and an optional retry after approval', async () => {
    apiMocks.saveLessonStep.mockResolvedValueOnce({
      data: { current_step: 3, completed_steps: [0, 1, 2], mission_completed: true },
    })
    apiMocks.getLesson.mockResolvedValue({
      data: {
        ...baseLesson,
        current_step: 3,
        completed_steps: [0, 1, 2],
        status: 'completed',
        score_percent: 80,
        passed: true,
        attempt_finished: true,
        must_retry: false,
        can_retry_optionally: false,
        progress: {
          mission_id: 10,
          status: 'completed',
          score: 70,
          score_percent: 80,
          attempts: 1,
          started_at: null,
          completed_at: null,
        },
        next_mission: { id: 11, number: 2, name: 'O que importa primeiro?' },
      },
    })

    renderLesson()

    expect(await screen.findByText('80%')).toBeInTheDocument()
    expect(screen.getByText('Aprovado ✓')).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: /Próximo módulo: O que importa primeiro/ }),
    ).toBeInTheDocument()

    fireEvent.click(
      screen.getByRole('button', { name: /Refazer módulo \(opcional\)/ }),
    )
    await waitFor(() => expect(apiMocks.retryMission).toHaveBeenCalledWith(10, true))
  })

  it('offers an exit confirmation and keeps progress saved', async () => {
    apiMocks.getLesson.mockResolvedValue({
      data: { ...baseLesson, current_step: 1, completed_steps: [0], status: 'in_progress' },
    })

    renderLesson()

    fireEvent.click(await screen.findByRole('button', { name: 'Sair do módulo' }))
    expect(screen.getByRole('dialog', { name: 'Sair do módulo?' })).toBeInTheDocument()
    expect(screen.getByText(/já foi salvo/)).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Sair agora' }))
    expect(await screen.findByText('Minha jornada')).toBeInTheDocument()
  })
})
