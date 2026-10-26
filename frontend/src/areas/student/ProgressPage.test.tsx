import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { ProgressPage } from './ProgressPage'

const apiMocks = vi.hoisted(() => ({
  getSummary: vi.fn(),
}))

vi.mock('@/api', () => ({
  progressApi: { getSummary: apiMocks.getSummary },
}))

describe('ProgressPage', () => {
  beforeEach(() => {
    apiMocks.getSummary.mockResolvedValue({
      data: {
        total_points: 150,
        coins: 24,
        level: 1,
        level_name: 'Iniciante',
        current_level_points: 0,
        next_level_points: 300,
        achievements: [
          { key: 'primeiro_passo', name: 'Primeiro passo', earned_at: '2026-10-21T00:00:00Z' },
        ],
        competencies: [
          {
            code: '1.1.1',
            name: 'Distinguir salário bruto de líquido',
            status: 'demonstrated',
            correct_count: 1,
            incorrect_count: 0,
            reinforcement_suggested: false,
          },
        ],
        missions_completed: 1,
        missions_in_progress: 0,
        analyst_insight: {
          agent: 'analyst',
          severity: 'positive',
          action: 'advance',
          competencies: ['Distinguir salário bruto de líquido'],
          message: 'Você demonstrou o conceito nesta etapa.',
        },
      },
    })
  })

  it('shows level, competency evidence and achievements from the API', async () => {
    render(
      <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <ProgressPage />
      </MemoryRouter>,
    )

    expect(await screen.findByRole('heading', { name: 'Iniciante' })).toBeInTheDocument()
    expect(screen.getByText('Distinguir salário bruto de líquido')).toBeInTheDocument()
    expect(screen.getByText('Primeiro passo')).toBeInTheDocument()
    expect(screen.getByText('1 missão concluída')).toBeInTheDocument()
    expect(screen.getByText('24')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Prismas · Ir para o Estúdio/ })).toBeInTheDocument()
    expect(screen.getAllByText('1 competência demonstrada')).toHaveLength(2)
    expect(screen.getByText('Você demonstrou o conceito nesta etapa.')).toBeInTheDocument()
  })
})
